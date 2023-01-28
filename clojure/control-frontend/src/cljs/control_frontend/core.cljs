(ns control-frontend.core
  (:require
    [control-frontend.config :as config]
    [control-frontend.events :as events]
    [control-frontend.views :as views]
    [re-frame.core :as re-frame]
    [reagent.core :as reagent]
    ))


(defn dev-setup []
  (when config/debug?
    (println "dev mode")))

(defn ^:dev/after-load mount-root []
  (re-frame/clear-subscription-cache!)
  (reagent/render [views/main-panel]
                  (.getElementById js/document "app")))

(defn init []
  (re-frame/dispatch-sync [::events/initialize-db])
  (dev-setup)
  (mount-root))
