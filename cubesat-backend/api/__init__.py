"""
Welcome to the documentation for the Alpha CubeSat project's Ground Station backend software!

### Overview

This is the Ground Station software for the Alpha CubeSat project. It is a full-stack web app
developed using Python/Flask for the backend and React.js for the frontend UI.

The backend receives data from the RockBlock API, processes that data, and sends it to ElasticSearch.
It is architected as a RESTful server with multiple modules that each provide functionality for specific services
such as receiving telemetry, authentication, sending issuing commands, and viewing captures.

The frontend UI allows you to select commands using dropdowns, fill in any fields, validate them,
and send them to the backend, which in turn uses RockBlock web services to send them to the CubeSat.
Additional features include sending multiple commands at once, drag/drop command reordering,
a log of previously sent commands, and an capture viewer for downlinked captures.

See the [GitHub README](https://github.com/Alpha-CubeSat/Alpha-Cubesat-Ground-Python)
for more detailed information about setup and usage.
"""

from api.app import create_app