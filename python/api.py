from flask import Flask, request, make_response
from markupsafe import escape

app = Flask(__name__)

@app.get('/api/debug/ping')
def ping():
    return 'pong'

@app.post('/api/debug/echo')
def echo():
    return escape(request.data)

@app.post('/api/auth/login')
def login():
    return make_response('Login not configured yet.', 503)

@app.post('/api/rockblock/telemetry')
def rockblock_telemetry():
    return make_response('Telemetry not configured yet.', 503)

@app.get('/api/cubesat/img/recent')
def get_recent_images():
    return make_response('API not configured yet.', 503)

@app.get('/api/cubesat/img/<name>')
def get_image():
    return make_response('API not configured yet.', 503)

@app.post('/api/cubesat/command')
def uplink_command():
    return make_response('API not configured yet.', 503)
