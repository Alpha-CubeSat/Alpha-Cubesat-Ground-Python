# Alpha CubeSat Ground
Ground Station software for the Alpha CubeSat project

## Overview
This is the Ground Station software for the Alpha CubeSat project. It is a full-stack web app
developed using Python/Flask for the backend and React.js for the frontend UI.

The backend receives data from the RockBlock API, processes that data, and sends it to ElasticSearch. 
It is architected as a RESTful server with multiple modules that each provide functionality for specific services 
such as receiving telemetry, authentication, sending issuing commands, and viewing images. 

The frontend UI allows you to select commands using dropdowns, fill in any fields, validate them, 
and send them to the backend, which in turn uses RockBlock web services to send them to the CubeSat. 
Additional features include sending multiple commands at once, drag/drop command reordering, 
a log of previously sent commands, and an image viewer for downlinked images.

This repo is a rewrite (along with new features) of the [previous version](https://github.com/Alpha-CubeSat/Alpha-Cubesat-Ground-Clojure) 
of the ground station software in Clojure.

## Dependencies
- Python version >= 3.9
- NodeJS >= 18.0
- Python dependencies (run `pip install -r requirements.txt`)
- React/JS dependencies (run `npm install`)

## Setting up the Ground Station for Development
This section provides instructions on setting up the environment and running the ground software for development/testing purposes.
Both the frontend and backend use frameworks that support code hotloading, so simply making changes to the code will update
the running ground software, so long as it is started in development mode. This makes for a convenient development experience, 
and it is recommended to keep the ground software and environment running while developing as changes in code will be loaded 
without the need to recompile/reboot anything.

*Note: Alpha runs its ground software on Ubuntu Server, so if you are using something else, such as Windows, the locations of ElasticSearch and Kibana configuration files might be elsewhere.*

1. **Install ElasticSearch.**
ElasticSearch is what the ground system uses to store telemetry data received from the satellite. 
A guide for installation can be found in [Elastic's documentation](https://www.elastic.co/guide/en/elasticsearch/reference/current/install-elasticsearch.html). 
Then, configure ElasticSearch as necessary (configuration at `/etc/elasticsearch/elasticsearch.yml`). 
By default it will listen on `localhost:9200`.


2. **Install Kibana.**
Kibana is a visualization tool for creating graphics and timeseries out of data in ElasticSearch. 
This will be useful for configuring alerts, graphs, and other aggregations of telemetry data.
A guide for installation can be found in [Elastic's documentation](https://www.elastic.co/guide/en/kibana/current/install.html). 
Kibana can be configured as needed in the configuration file (at `/etc/kibana/kibana.yml`). 
By default Kibana listens on `localhost:5601`.  


3. **Configure the Backend Server.**
Navigate to `cubesat-backend` and configure the backend by creating an `.env` file in the folder. You will need to configure the following environmental variables:
    - `ROCKBLOCK_USER`, `ROCKBLOCK_PASS`: The username and password of the RockBlock Web Services account used for receiving telemetry and sending commands.
    - `GS_ADMIN_PASS`: The password for the ground station's admin user.
    - `ELASTIC_USER`, `ELASTIC_PASS`: The username and password of the Elasticsearch superuser account.
    - `ELASTIC_CERTS`: The filepath to Elasticsearch's HTTPS certificates, usually located in `<elasticsearch base path>/config/certs/http_ca.crt`.

4. **Run the Backend Server.**
Run the command `flask run`. This will start the backend server that listens for requests at `localhost:5000`.
The server will run in development mode, so it hotloads code: if you make a change,
the new code will be injected (and start running) into the already running server when you save a file in your editor.
An interactive API documentation will also be generated when the development server is booted, which can be found at `/docs`.  


5. **Configure the Frontend.**
Navigate to `cubesat-frontend` and configure the frontned by creating an `.env` file in the folder. You will need to configure the following environmental variables:
    - `REACT_APP_BASE_API_URL`: The URL of the backend server that the frontend makes API requests to.
    - `REACT_APP_KIBANA_URL`: The URL of the Kibana server (used form the base URL for viewing normal reports in Kibana).
    - `REACT_APP_KIBANA_NR_DOC_ID`: The ID of the Kibana `cubesat_normal_report` document (used form the base URL for viewing normal reports in Kibana).

7. **Run the Frontend UI.**
Once configured, run the command `npm start` (make sure the back-end is still running).
This will start the fronend server which is assessable at `localhost:3000`.
Again, frontend code is hotloaded, so leave the UI open as you develop, and changes to the code will be uploaded to the browser and 
reflected in the UI without the need to refresh the page in the browser or manually rerun/rebuild any code.

## Setting up the Ground Station for Production
There are some tasks and configuration, such as building the code for production, that are outlined here. These will help you set up the ground station in a production environment that serves and runs optimized code, and is configured to be secure.

TODO: Update

- **Build the backend code** in `cubesat-backend` by running `lein do clean, ring uberjar`. This will produce a jar file under `target/` containing the backend and all dependencies to be run stand-alone when you deploy it.
- **Build the frontend code** in `control-frontend` by running `lein prod`. This will produce the production JavaScript code, and all other assets for the UI under `resources/public`. This will also produce a standalone jar that serves it under `target/`, containing everything.
- You will run into the request routing issue with the frontend again in a production environment - the UI will make API requests to the UI server when it needs to access the real backend server. So it is recommended to **use a reverse proxy** such as nginx to group everything under one service, and have the API requests be routed where they need to go. However, if you wish to host it from a subdirectory when you configure the proxy, the ground software currently doesn't allow configuration of the base url, so you will need to hardcode it. Support for this is coming soon (see "work in progress" section).
- While you are at it, **host kibana behind a reverse proxy**. Again, if you host it at a subdirectory, you will need it to make requests to the new route. This can be configured by changing the `server.basePath` configuration to the name of your desired path in `kibana.yml`.
- **Secure the Elastic Stack**. Secure kibana by going to the configuration file, and adding `xpack.security.enabled: true`. This will enable Kibana authentication. Then, go to the ElasticSearch configuration file, and add: `xpack.security.enabled: true` and (only if you are running a single node, you will need TLS for a cluster, which is not covered here) `discovery.type: single-node`. Now, navigate to the ElasticSearch installation and run `bin/elasticsearch-setup-passwords interactive`. This will prompt you for passwords for all the default users, including the `kibana` and `elastic` users. Now for Kibana to communicate with ElasticSearch, it must authenticate as the `kibana` user. To allow it to do this, return to the Kibana config, and add `elasticsearch.username: "kibana"` and `elasticsearch.password: "<password>"` where `<password>` is the password you just set for the `kibana` user.
The default superuser on Kibana is `elastic` with the password you just set. You can manage/create/remove users, change passwords, and determine roles in the Kibana UI by navigating to the options panel (⚙) and clicking on "security". Create a role with the name of your choice that has all permissions on the indices you configured in `config.edn` for telemetry data. Then create a user with this role, and alter `config.edn` to use its credentials. 
- **Secure the ground system** -- Navigate to the tools project `cubesat-clitools` and build it with `lein uberjar`. Then run the resulting jar, which will prompt you to create some user credentials. It will accept the name of an output file as an argument. Once finished, change the `:users-file` configuration in the configuration file, and the backend will require authentication with any of the credentials in the new file. `cubesat-clitools` can also be used to create and manage users for this file.
- **Beware of missing or unfinished features**. This software is still being developed for Alpha's mission. So some features may be missing. Check the following section for more information.
