from flask import Blueprint, make_response

cubesat = Blueprint('cubesat', __name__)

@cubesat.get('/img/recent')
def get_recent_images():
    return make_response('API not configured yet.', 503)

@cubesat.get('/img/<name>')
def get_image(name):
    return make_response('API not configured yet.', 503)

@cubesat.post('/command')
def uplink_command():
    return make_response('API not configured yet.', 503)