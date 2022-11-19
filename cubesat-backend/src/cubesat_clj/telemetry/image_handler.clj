(ns cubesat-clj.telemetry.image-handler
  (:require [clojure.java.io :as io]
            [cubesat-clj.databases.image-database :as img]
            [cubesat-clj.util.binary.hex-string :as bin]
            [ring.util.http-response :as http]
            [schema.core :as s])
  (:import (org.apache.commons.io IOUtils)))


(s/defschema ImageData
  {:name   s/Str
   :date   s/Inst
   :base64 s/Str})


(s/defschema ImageNames
  [s/Str])


(defn get-image-data
  [image-file]
  (println "ih: get-image-data")
  (let [b64 (-> image-file
                (io/input-stream)
                (IOUtils/toByteArray)
                (bin/bytes-to-b64))
        date (.lastModified image-file)
        name (.getName image-file)]
    {:name   name
     :date   (Date. date)
     :base64 b64}))


(defn get-image-at [idx]
  (println "ih: get-image-at")
  (-> (img/get-recent-images (inc idx))
      (nth idx)
      (get-image-data)))


(defn get-image-by-name [name]
(println "ih: get-image-by-name")
  (get-image-data (img/get-image-by-name name)))


(defn get-recent-image-names [n]
(println "ih: get-recent-image-names")
  (->> (img/get-recent-images n)
       (map #(.getName %))
       vec))


(defn handle-get-image-list [count]
(println "ih: get-image-list")
  (http/ok (get-recent-image-names count)))


(defn handle-image-request [name]
(println "ih: handle-image-request")
  (http/ok (get-image-by-name name)))

