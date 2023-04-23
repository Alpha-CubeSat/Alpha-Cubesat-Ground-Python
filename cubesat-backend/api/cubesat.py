import time

from apifairy import response, authenticate, arguments, body, other_responses
from flask import Blueprint

import control.control_handler as control
import databases.image_database as image_db
from api.auth import token_auth
from api.schemas import ImageNameSchema, ImageCountSchema, ImageDataSchema, CommandSchema, \
    CommandResponseSchema

cubesat = Blueprint('cubesat', __name__)

@cubesat.get('/img/recent')
@authenticate(token_auth)
@arguments(ImageCountSchema)
@response(ImageNameSchema)
@other_responses({401: 'Invalid access token'})
def get_recent_images(args):
    """
    Get Recent Images
    Returns a list of names of recently received ttl files
    """
    return {'images': image_db.get_recent_images(args['count'])}

@cubesat.get('/img/<name>')
@authenticate(token_auth)
@response(ImageDataSchema)
@other_responses({401: 'Invalid access token'})
def get_image(name: 'Name of the image'):
    """
    Get Image By Name
    Returns the ttl file with the given name if it exists
    """
    return image_db.get_image_data(name)

@cubesat.post('/command')
@authenticate(token_auth)
@body(CommandSchema(many=True))
@response(CommandResponseSchema)
@other_responses({401: 'Invalid access token'})
def uplink_command(command):
    """
    Uplink Command
    Process a command to be sent to cubesat
    """
    print(command)
    uplink_response = control.handle_command(command)

    # for basic integration testing only
    return {
        'status': 'success' if uplink_response.find("OK") != -1 else 'failure',
        'timestamp': time.time() * 1000,
        'commands': command,
        'message': uplink_response
    }

@cubesat.get('/command')
@authenticate(token_auth)
# @body(CommandSchema)
# @response(CommandResponseSchema)
@other_responses({401: 'Invalid access token'})
def get_command_history(command):
    """
    Get Command History
    Get all previously sent commands to the CubeSat
    """
    return 'API not configured yet.', 503