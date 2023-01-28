"""
Welcome to the documentation for the Alpha CubeSat project's Ground Station backend software!

### Overview

This is the Ground Station software for the AlphaCubesat project. It is a full-stack application with code for frontend UI and backend.

The backend receives data from the RockBlock API, processes that data, and ships it to ElasticSearch. It is architected as a RESTful server with multiple modules that each provide functionality for specific services such as receiving telemetry, authentication, and issuing commands.

The UI is a work in progress but allows you to select from a set of commands, fill in fields, validate them, and send them to the backend, which in turn uses RockBlock web services to issue them to the satellite. Additional features such as a log of sent commands, macros, and scheduling on a visual timeline are not yet present, but will be.
"""

from api.app import create_app