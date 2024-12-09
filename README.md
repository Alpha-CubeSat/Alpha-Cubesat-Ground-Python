# Alpha CubeSat Ground
Ground Station software for the Alpha CubeSat project

## Overview
This is the Ground Station software for the Alpha CubeSat project. It is a full-stack web app
developed using Python/Flask for the backend and React.js for the frontend UI.

The backend receives data from the RockBlock API, processes that data, and sends it to ElasticSearch. 
It is architected as a RESTful server with multiple modules that each provide functionality for specific services 
such as receiving telemetry, authentication, sending issuing commands, and viewing captures. 

The frontend UI allows you to select commands using dropdowns, fill in any fields, validate them, 
and send them to the backend, which in turn uses RockBlock web services to send them to the CubeSat. 
Additional features include sending multiple commands at once, drag/drop command reordering, 
a log of previously sent commands, and an capture viewer for downlinked captures.

This repo is a rewrite (along with new features) of the [previous version](https://github.com/Alpha-CubeSat/Alpha-Cubesat-Ground-Clojure) 
of the ground station software in Clojure.

## Dependencies
- Python version >= 3.9
- NodeJS >= 18.0
- Python dependencies (run `pip install -r requirements.txt`)
- React/JS dependencies (run `npm install`)

## Setting up the Ground Station for Development
This section provides instructions on setting up the environment and running the ground software for local development/testing purposes.

*Note: Alpha runs its ground software on Ubuntu Server, so if you are using something else, such as Windows, the locations of Elasticsearch and Kibana configuration files might be elsewhere.*

1. **Install ElasticSearch.**
ElasticSearch is what the ground system uses to store telemetry data received from the satellite. 
A guide for installation can be found in [Elastic's documentation](https://www.elastic.co/guide/en/elasticsearch/reference/current/install-elasticsearch.html). 
Then, configure ElasticSearch as necessary (configuration at `/etc/elasticsearch/elasticsearch.yml`). 
By default Elasticsearch will listen on `localhost:9200`.

2. **Install Kibana.**
Kibana is a visualization tool for creating graphics out of data in ElasticSearch. 
This will be useful for configuring alerts, graphs, and other aggregations of telemetry data.
A guide for installation can be found in [Kibana's documentation](https://www.elastic.co/guide/en/kibana/current/install.html). 
Kibana can be configured as needed in the configuration file (at `/etc/kibana/kibana.yml`). 
By default Kibana will listen on `localhost:5601`.  

3. **Configure the Backend Server.**
Navigate to `cubesat-backend` and configure the backend by creating an `.env` file in the folder. You will need to configure the following environmental variables:
    - `ROCKBLOCK_USER`, `ROCKBLOCK_PASS`: The username and password of the RockBlock Web Services account used for receiving telemetry and sending commands.
    - `GS_ADMIN_PASS`: The password for the ground station's admin user.
    - `ELASTIC_USER`, `ELASTIC_PASS`: The username and password of the Elasticsearch superuser account.
    - `ELASTIC_CERTS`: The filepath to Elasticsearch's HTTPS certificates, usually located in `<elasticsearch base path>/config/certs/http_ca.crt`.

4. **Run the Backend Server.**
Run the command `flask run`. This will start the backend server that listens for requests at `localhost:5000`.
On first run, it many neccessary to run the `flask init-db` command to setup the user database.
An interactive API documentation playground will also be generated when the development server is booted, which can be found at `/docs`.  

5. **Configure the Frontend.**
Navigate to `cubesat-frontend` and configure the frontned by creating an `.env` file in the folder. You will need to configure the following environmental variables:
    - `REACT_APP_BASE_API_URL`: The URL of the backend server that the frontend makes API requests to.
    - `REACT_APP_KIBANA_URL`: The URL of the Kibana server (used to form the base URL for viewing normal reports in Kibana).
    - `REACT_APP_KIBANA_NR_DOC_ID`: The ID of the Kibana `cubesat_normal_report` document (used to form the base URL for viewing normal reports in Kibana).

7. **Run the Frontend UI.**
Once configured, run the command `npm start` (make sure the backend server is still running).
This will start the fronend server which is assessable at `localhost:3000`.

## Setting up the Ground Station for Production
There are some tasks and configuration need to fully setup the production version of the ground station on a Linux machine. The files needed for this section can be found under the `hosting-related/` folder.

1. **Setup Services.** Ensure steps 1, 2, 3, and 5 from above have been completed. To import the Kibana dashboards, navigate to `<Kibana base URL>/app/management/kibana/objects` and import `cubesat_dashboard.ndjson` and `chipsat_dashboard.ndjson`.
2. **Setup Backend and Frontend as Services.** Copy the `gs-backend.service` and `gs-ui.service` files into `/etc/systemd/system/`. Modify the `WorkingDirectory` path as needed. These files allow the ground station services to start automatically on boot. They also should automatically restart each process when the code is updated. Logs can be accessed through `journalctl -u <gs-backend | gs-ui>.service --since today`.
3. **Setup Nginx Reverse Proxy.** Install Nginx, copy the `nginx-config.txt` file into `/etc/nginx/sites-available`, and rename it to `default`. This assumes the services are running at thier default ports. Use  [Certbot](https://certbot.eff.org/instructions?ws=nginx&os=snap) to setup HTTPS and modify the domain name as needed. Copy the contents of the `nginx_landing` folder to `/usr/share/nginx/html/`.
4. **Secure the Elastic Stack.** Secure Elasticsearch and Kibana by going to their configuration files and adding `xpack.security.enabled: true` (should be enabled by default). Then, navigate to `<Kibana base URL>/app/management/security/users` and add an `admin` user wih roles `superuser` and `kibana_system`. Create other users as needed.
5. **Add Users to Ground Station UI.** Navigate to `<GS base URL>/ui` and log in as the `admin` user (defined in backend config file). Click on `Settings` in the upper right corner and `ADMIN: Edit Users` to create additional user logins.
