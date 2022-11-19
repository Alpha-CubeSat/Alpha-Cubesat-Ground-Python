(ns cubesat-clj.telemetry.cubesat-telemetry
  "Specifies/parses formats used by the RockBlock API and cubesat.
  These formats are described in the RockBlock web services docs at:
  https://docs.rock7.com/reference#push-api
  And for the satellite in the Google Drive for Alpha"
  (:require [clojure.string :as str]
            [cubesat-clj.config :as cfg]
            [cubesat-clj.databases.elasticsearch :as es]
            [cubesat-clj.databases.image-database :as img]
            [cubesat-clj.telemetry.rockblock-telemetry :as rb]
            [cubesat-clj.util.binary.binary-reader :as reader]
            [cubesat-clj.util.binary.hex-string :as hex]))

(def ^:const opcodes
  "Packet opcodes for cubesat (see Alpha documentation for specification)"
  {99  ::normal-report
   24  ::deployment-report
   42  ::ttl})

(defn save-cubesat-data
  "Saves a cubesat report to elasticsearch"
  [data]
  (println "cs: save-cubesat-data")
  (let [index (cfg/cubesat-db-index (cfg/get-config))]
    (es/index! index es/daily-index-strategy data)))

(defn- map-range
  "Recreation of Arduino map() function used in flight code in order to convert imu data to correct imu values.
  https://www.arduino.cc/reference/en/language/functions/math/map/"
  [x in-min in-max out-min out-max]
  (println "cs: map-range")
  (+ out-min
     (* (/ (- out-max out-min)
           (- in-max in-min))
        (- x in-min))))

;;================================================================================================
;; fragment-number is the number of the fragment
;; fragment-list is a list of different fragment numbers received
;; fragment-data is the Hex String downlinked from the IMU. Includes fragment number, x-gyro values, y-gyro values, z-gyro values
(def fragment-list (atom {:list []}))

(def imu-display-info (atom {:latest-fragment 0
                             :missing-fragments "None"
                             :highest-fragment 0}))

(defn- generate-missing-fragments 
  "Finds the missing fragments and the highest fragment received for IMU deployment downlinks. 
  It counts through all already-received fragments every time because fragments could be receieived in random order."
  [frag-list]
  (println "cs: generate-missing-fragments")
  (let [max-frag (apply max frag-list)]
    (swap! imu-display-info assoc :missing-fragments "")
    (swap! imu-display-info assoc :highest-fragment max-frag)
    (loop [x 0]
      (when (< x max-frag)
        (if (some #(= x %) frag-list)
          ()
          (let [missing-frags (:missing-fragments @imu-display-info)]
            (swap! imu-display-info assoc :missing-fragments (str missing-frags x " "))))
        (recur (inc x))))
    (if (= (count (:missing-fragments @imu-display-info)) 0) (swap! imu-display-info assoc :missing-fragments "None") ())))

(defn- compute-cycle-values    
  [{:keys [x-gyro y-gyro z-gyro] :as cycle-data}]
  (println "cs: compute-cycle-values")
  (assoc cycle-data
         :x-gyro (map-range (float x-gyro) 0 255 -180 180)
         :y-gyro (map-range (float y-gyro) 0 255 -180 180)
         :z-gyro (map-range (float z-gyro) 0 255 -180 180)))

(defn save-cycle-report 
  [cycle-data]
  (println "cs: save-cycle-report")
  (let [index (cfg/cycle-db-index (cfg/get-config))]
    (es/index! index es/daily-index-strategy cycle-data)))

(defn- separate-cycles
  [fragment-number fragment-data]
  (println "cs: seperate-cycles")        
  (let [frag-size (count fragment-data)]
      (loop [x 0]
        (when (< x frag-size)
          (let [second-index (+ x 2)
                third-index (+ x 4)
                fourth-index (+ x 6)
                x-gyro (Integer/parseInt (subs fragment-data x second-index) 16)
                y-gyro (Integer/parseInt (subs fragment-data second-index third-index) 16)
                z-gyro (Integer/parseInt (subs fragment-data third-index fourth-index) 16)
                raw-cycle-values {:x-gyro x-gyro, :y-gyro y-gyro, :z-gyro z-gyro}
                cycle-count (+ (* fragment-number 22) (/ x 6))] ;; every full fragment has 22 cycles, new cycle occurs every six digits in the hex string
            
                (save-cycle-report (merge (compute-cycle-values raw-cycle-values) {:cycle-count cycle-count})))
          (recur (+ x 6))))))

(defn save-deploy-report
  [data]
  (println "cs: save-deploy-report")
  (let [index (cfg/deploy-db-index (cfg/get-config))]
    (es/index! index es/daily-index-strategy data)))

(defn process-deploy-data
  "Saves a deployment report to elasticsearch"
  [data]
  (println "cs: process-deploy-data")
  (let [{:keys [imei transmit-time fragment-number fragment-data]} data
        meta {:imei imei :transmit-time transmit-time}
        newlist (conj (:list @fragment-list) fragment-number)]
    (swap! fragment-list assoc :list newlist) ;; add fragment to list
    (generate-missing-fragments (:list @fragment-list))
    (separate-cycles fragment-number fragment-data)
    (save-deploy-report (merge meta @imu-display-info))))

;;=================================================================================================

(defn save-image-data
  "Saves an image fragment report to elasticsearch"
  [data]
  (println "cs: save-image-data")
  (let [index (cfg/image-db-index (cfg/get-config))]
    (es/index! index es/daily-index-strategy data)))

(defn process-ttl-data
  "Process image fragment data sent by cubesat. Image comes over several fragments as
  rockblock only supports so much protocol. Image 'fragments' are then assembled into full images
  when fully collected, and saved into the image database"
  [ttl-data]
  (println "cs: process-ttl-data")
  (let [{:keys [imei transmit-time serial-number fragment-number fragment-data max-fragments]} ttl-data
        meta {:imei imei :transmit-time transmit-time}]
    (img/save-fragment serial-number fragment-number fragment-data)
    (img/try-save-image serial-number max-fragments)
    (let [data (img/get-img-display-info)]
      (save-image-data (merge meta data)))))

(defn- read-opcode
  "Reads the opcode of an incoming packet. If empty packet is received, returns ::empty-packet instead"
  [packet]
  (println "cs: read-opcode")
  (if (= (reader/remaining packet) 0)
    ::empty-packet
    (-> packet
        (reader/read-uint8)
        opcodes)))

(defn- read-img-hex-fragment
  "Reads the hexadecimal string of an image fragment to determine if the 
   fragment is the last fragment, which is indicated by the end-marker 'ffd9'. 
   Returns the serial number in decimal form, the fragment number in 
   decimal form, the max number of fragments in decimal form, and the hex string 
   of fragment data needed to be read (minus the opcode, image serial number and 
   fragment number).
   
   If the image fragment is not last, then the max number of fragments is set 
   arbitrarilty to -1, and the entirety of the fragment portion in hex string 
   must be read. If the image fragment is the last, then the max number of 
   fragments is set to (last fragment number + 1), and the hexadecimal string is 
   read up to 'ffd9'.
   
   Notes: 
          - The hex string is the data report minus the op code at the beginning
            (so everything after the op code from the downlink).
          - The serial number is stored in the indices of [0, 2) of the hex 
            string.
          - The fragment number is stored in the indices [8, 10) of the hex 
            string. Fragment count starts at 0.
          - The fragment data starts at index 10 and goes to the end of of the
            hex-string or to the end of end-marker 'ffd9'.
          - The entire hex string for an image fragment data is 69 bytes long 
            (138 characters)."
  [rockblock-data]
  (println "cs: read-img-hex-fragment")
  (let [serial-number (Integer/parseInt (subs rockblock-data 0 2) 16)
        fragment-number (Integer/parseInt (subs rockblock-data 8 10) 16)
        end-marker-index (str/index-of rockblock-data "ffd9")
        max-fragments (if (nil? end-marker-index) -1 (+ fragment-number 1))
        end-boundary (if (nil? end-marker-index) 138 (+ end-marker-index 4))
        fragment-data (hex/hex-str-to-bytes (subs rockblock-data 10 end-boundary))]
      {:serial-number serial-number, :fragment-number fragment-number, :max-fragments max-fragments, :fragment-data fragment-data}))

(defn- compute-normal-report-values
  [{:keys [burnwire-burn-time burnwire-armed-timeout-limit burnwire-attempts downlink-period x-mag y-mag z-mag x-gyro y-gyro z-gyro temp solar-current battery-voltage] :as cubesat-data}]
  (println "cs: compute-normal-report-values")
  (assoc cubesat-data
         :burnwire-burn-time (map-range (float burnwire-burn-time) 0 255 0 60000)
         :burnwire-armed-timeout-limit (map-range (float burnwire-armed-timeout-limit) 0 255 0 86400000)
         :burnwire-attempts (map-range (float burnwire-attempts) 0 255 0 10)
         :downlink-period (map-range (float downlink-period) 0 255 1000 172800000)
         :x-mag (map-range (float x-mag) 0 255 -180 180)
         :y-mag (map-range (float y-mag) 0 255 -180 180)
         :z-mag (map-range (float z-mag) 0 255 -180 180)
         :x-gyro (map-range (float x-gyro) 0 255 -180 180)
         :y-gyro (map-range (float y-gyro) 0 255 -180 180)
         :z-gyro (map-range (float z-gyro) 0 255 -180 180)
         :temp (map-range (float temp) 0 255 0 200)
         :solar-current (map-range (float solar-current) 0 255 0 500)
         :battery-voltage (map-range (float battery-voltage) 0 255 3 5)))

(defn- read-imu-hex-fragment
  [rockblock-data]
  (println "cs: read-imu-hex-fragment")
  (let [fragment-number (Integer/parseInt (subs rockblock-data 0 2) 16)
        fragment-data (subs rockblock-data 2)]
      {:fragment-number fragment-number :fragment-data fragment-data}))

(defmulti read-packet-data
  "Reads data from a packet based on opcode.
          Note: Image data is received in fragments, :data-length bytes each, which must be assembled into a full image
          after receiving all fragments. The serial number is which image is being sent, and the fragment number
          is which part of the image being sent"
  (fn [[opcode rockblock-data]] opcode))

(defmethod read-packet-data ::ttl
  [[_ rockblock-data]]
  (println "cs: read-packet-data ttl")
  (read-img-hex-fragment rockblock-data))

(defmethod read-packet-data ::normal-report
  [[_ packet]]
  (println "cs: read-packet-data normal-report")
  (-> packet
      (reader/read-structure
       [:is-photoresistor-covered ::reader/uint8
        :is-door-button-pressed ::reader/uint8
        :mission-mode ::reader/uint8
        :fire-burnwire ::reader/uint8
        :arm-burnwire ::reader/uint8
        :burnwire-burn-time ::reader/uint8
        :burnwire-armed-timeout-limit ::reader/uint8
        :burnwire-mode ::reader/uint8
        :burnwire-attempts ::reader/uint8
        :downlink-period ::reader/uint8
        :waiting-messages ::reader/uint8
        :is-command-waiting ::reader/uint8
        :x-mag ::reader/uint8
        :y-mag ::reader/uint8
        :z-mag ::reader/uint8
        :x-gyro ::reader/uint8
        :y-gyro ::reader/uint8
        :z-gyro ::reader/uint8
        :temp ::reader/uint8
        :temp-mode ::reader/uint8
        :solar-current ::reader/uint8
        :in-sun ::reader/uint8
        :acs-mode ::reader/uint8
        :battery-voltage ::reader/uint8
        :fault-mode ::reader/uint8
        :check-x-mag ::reader/uint8
        :check-y-mag ::reader/uint8
        :check-z-mag ::reader/uint8
        :check-x-gyro ::reader/uint8
        :check-y-gyro ::reader/uint8
        :check-z-gyro ::reader/uint8
        :check-temp ::reader/uint8
        :check-solar-current ::reader/uint8
        :check-battery ::reader/uint8
        :take-photo ::reader/uint8
        :camera-on ::reader/uint8])
        compute-normal-report-values))

(defmethod read-packet-data ::deployment-report
  [[_ rockblock-data]]
  (println "cs: read-packet-data deployment-report")
  (read-imu-hex-fragment rockblock-data))

(defn- report-metadata
  "Returns rockblock metadata such as transmit time from a rockblock report as a map"
  [rockblock-report]
  (println "cs: report-metadata")
  (let [{:keys [imei transmit_time]} rockblock-report]
    {:imei          imei
     :transmit-time transmit_time}))

(defn- error-data
  "Returns a map containing a cubesat report with the error opcode, raw data, and an error message"
  [rockblock-report error-msg]
  (println "cs: error-data")
  {:telemetry-report-type ::error
   :error    error-msg
   :raw-data (:data rockblock-report)})

(defn read-cubesat-data
  "Reads the cubesat data inside a rockblock report. Returns a map containing the data if read, or an error report
  if the packet is empty or some issue occurred. If the data is successfully read, the opcode is returned in the
  result map as :telemetry-report-type. Otherwise :telemetry-report-type is set to ::error"
  [rockblock-report]
  (println "cs: read-cubesat-data")
  (let [packet (rb/get-cubesat-message-binary rockblock-report)
        op (read-opcode packet)
        rockblock-data (subs (:data rockblock-report) 2)
        meta (report-metadata rockblock-report)
        result (if (= op ::empty-packet)
                 (error-data rockblock-report "empty packet")
                 (try
                    (if (= op ::normal-report)
                    (assoc (read-packet-data [op packet]) :telemetry-report-type op)
                    (assoc (read-packet-data [op rockblock-data]) :telemetry-report-type op)) ;; rockblock-data is hex string with op code removed
                   (catch Exception e (error-data rockblock-report (.getMessage e)))))]
    (merge meta result)))