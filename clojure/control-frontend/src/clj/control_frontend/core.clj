(ns control-frontend.core
  (:require [config.core :refer [env]]
            [control-frontend.handler :refer [handler]]
            [ring.adapter.jetty :refer [run-jetty]])
  (:gen-class))

(defn -main [& args]
  (let [port (Integer/parseInt (or (env :port) "8000"))]
    (run-jetty handler {:port port :join? false})))
