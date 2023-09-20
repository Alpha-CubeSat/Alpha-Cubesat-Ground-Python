import json
import time
from os.path import exists

import jwt
from apifairy import response, authenticate, arguments, body, other_responses
from flask import Blueprint

from api.auth import token_auth
from api.schemas import ImageNameSchema, ImageCountSchema, ImageDataSchema, CommandSchema, \
    CommandResponseSchema, RockblockReportSchema
from control import control_protocol
from databases import image_database, elastic
from telemetry import process_telemetry
from telemetry.telemetry_constants import ROCKBLOCK_PK

cubesat = Blueprint('cubesat', __name__)

@cubesat.post('/telemetry')
@body(RockblockReportSchema)
@other_responses({401: 'Invalid JWT token'})
def rockblock_telemetry(report):
    """
    Rockblock Telemetry
    Used to receive downlinked data reports sent by the CubeSat from the RockBlock portal.
    Must have a valid JWT token.
    """
    print("report received")
    print(report)

    # Verifies the JWT token sent in a rockblock report
    # If JWT is invalid, handle exception and return 401/Unauthorized
    try:
        jwt.decode(report['JWT'], ROCKBLOCK_PK, algorithms=['RS256'])
    except:
        print('JWT verification error')
        return '', 401

    # Fixes the date format of the transmit_time field in the rockblock report.
    # Rockblock uses YY-MM-DD HH:mm:ss as the date format instead of the YYYY-MM-DDThh:mm:ssZ
    # standard format. Conversion is done by appending "20" to the start of the date string,
    # which means this fix may not work after the year 2100.
    report['transmit_time'] = f"20{report['transmit_time'].replace(' ', 'T')}Z"

    # Decode/process rockblock report and save it in elasticsearch
    process_telemetry.handle_report(report)  # wrap with try/catch in case of error?
    print("report processed")

    return '', 200 # Successful downlink code

@cubesat.get('/img/recent')
@authenticate(token_auth)
@arguments(ImageCountSchema)
@response(ImageNameSchema)
@other_responses({401: 'Invalid access token'})
def get_recent_imgs(args):
    """
    Get Recent Images
    Returns a list of names of all the fully downlinked image files received by the ground station.
    """
    return {'images': image_database.get_recent_images(args['count'])}

@cubesat.get('/img/<name>')
@authenticate(token_auth)
@response(ImageDataSchema)
@other_responses({401: 'Invalid access token'})
def get_image(name: 'Name of the image'):
    """
    Get Image By Name
    Returns the image file with the given name if it exists.
    """
    return image_database.get_image_data(name)

@cubesat.post('/command')
@authenticate(token_auth)
@body(CommandSchema(many=True))
@response(CommandResponseSchema)
@other_responses({401: 'Invalid access token'})
def uplink_command(command):
    """
    Uplink Command
    Process a command to be sent to the CubeSat via the RockBlock portal.
    Opcode, namespace, field, and value fields must be valid per the Alpha flight SW documentation.
    """
    print(command)
    uplink_response = control_protocol.handle_command(command)

    api_response = {
        'status': 'success' if uplink_response.find("OK") != -1 else 'failure',
        'timestamp': time.time() * 1000,
        'commands': command,
        'message': uplink_response
    }

    # log commands
    with open('command_log.txt', 'a') as f:
        f.write(json.dumps(api_response) + '\n')

    return api_response

@cubesat.get('/command_history')
@authenticate(token_auth)
@response(CommandResponseSchema(many=True))
@other_responses({401: 'Invalid access token'})
def get_command_history():
    """
    Get Command History
    Get all previously sent commands to the CubeSat via the RockBlock portal.
    """

    if not exists("command_log.txt"):
        return []

    history = []
    with open('command_log.txt') as f:
        for entry in f.readlines():
            history.append(json.loads(entry[:-1]))

    history.reverse()
    return history

@cubesat.get('/commandLog')
# @body(CommandSchema(many=True))
# @response(CommandResponseSchema)
@authenticate(token_auth)
@other_responses({401: 'Invalid access token'})
def get_processed_commands():
    """
    Get Processed Commands
    Get all previously sent commands to the CubeSat via the Rockblock portal
    that have been confirmed in the command log of the normal report.
    """
    return elastic.get_index("command_log")