from flask import Blueprint, make_response

rockblock = Blueprint('rockblock', __name__)

@rockblock.post('/telemetry')
def rockblock_telemetry():
    return make_response('Telemetry not configured yet.', 503)