from apifairy import response, authenticate, arguments, body, other_responses
from flask import Blueprint

from api.auth import token_auth
from api.schemas import ImageNameSchema, ImageCountSchema, ImageDataSchema, CommandSchema, \
    CommandResponseSchema

cubesat = Blueprint('cubesat', __name__)

@cubesat.get('/img/recent')
@authenticate(token_auth)
@arguments(ImageCountSchema)
@response(ImageNameSchema(many=True))
@other_responses({401: 'Invalid access token'})
def get_recent_images(query):
    """
    Get Recent Images
    Returns a list of names of recently received ttl files
    """
    return 'API not configured yet.', 503

@cubesat.get('/img/<name>')
@authenticate(token_auth)
@response(ImageDataSchema)
@other_responses({401: 'Invalid access token'})
def get_image(name: 'Name of the image'):
    """
    Get Image By Name
    Returns the ttl file with the given name if it exists
    """
    return 'API not configured yet.', 503

@cubesat.post('/command')
@authenticate(token_auth)
@body(CommandSchema)
@response(CommandResponseSchema)
@other_responses({401: 'Invalid access token'})
def uplink_command(request):
    """
    Uplink Command
    Process a command to be sent to cubesat
    """
    return 'API not configured yet.', 503