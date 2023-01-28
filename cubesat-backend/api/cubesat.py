from apifairy import response, authenticate, arguments, body, other_responses
from flask import Blueprint

import telemetry.image_handler as img
from api.auth import token_auth
from api.schemas import ImageNameSchema, ImageCountSchema, ImageDataSchema, CommandSchema, \
    CommandResponseSchema

# import control.control_handler as control

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
    return {'images': img.get_recent_image_names(args['count'])}

@cubesat.get('/img/<name>')
@authenticate(token_auth)
@response(ImageDataSchema)
@other_responses({401: 'Invalid access token'})
def get_image(name: 'Name of the image'):
    """
    Get Image By Name
    Returns the ttl file with the given name if it exists
    """
    return img.get_image_by_name(name)

@cubesat.post('/command')
@authenticate(token_auth)
@body(CommandSchema)
@response(CommandResponseSchema)
@other_responses({401: 'Invalid access token'})
def uplink_command(command):
    """
    Uplink Command
    Process a command to be sent to cubesat
    """
    # control.handle_command(command)
    return 'API not configured yet.', 503