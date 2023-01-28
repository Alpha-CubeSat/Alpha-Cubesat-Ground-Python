(ns control-frontend.handler
  (:require
    [compojure.core :refer [GET defroutes]]
    [compojure.route :refer [resources]]
    [ring.middleware.reload :refer [wrap-reload]]
    [ring.util.response :refer [resource-response]]
    [shadow.http.push-state :as push-state])
  (:gen-class))

(defroutes routes
  (GET "/" [] (resource-response "index.html" {:root "public"}))
  (resources "/"))

(def dev-handler (-> #'routes wrap-reload push-state/handle))

(def handler routes)
