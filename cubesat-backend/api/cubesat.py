import datetime
import json
import time
from os.path import exists

import jwt
from apifairy import response, authenticate, arguments, body, other_responses
from flask import Blueprint

import config
from api.auth import token_auth
from api.schemas import ImageNameSchema, ImageCountSchema, ImageDataSchema, \
    CommandResponseSchema, RockblockReportSchema, CommandUplinkSchema, DownlinkHistorySchema
from control import control_protocol
from control.control_constants import SFR_OVERRIDE_OPCODES_MAP, FAULT_OPCODE_MAP
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
    print('report received')
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
    process_telemetry.handle_report(report)
    print('report processed')

    return '', 200  # Successful downlink code


@cubesat.get('/img/<imei>/recent')
@authenticate(token_auth)
@arguments(ImageCountSchema)
@response(ImageNameSchema)
def get_recent_imgs(args, imei):
    """
    Get Recent Images
    Returns a list of names of all the fully downlinked image files received by the ground station.
    """
    return {'images': image_database.get_recent_images(imei, args['count'])}


@cubesat.get('/img/<imei>/<name>')
@authenticate(token_auth)
@response(ImageDataSchema)
@other_responses({400: 'Image does not exist'})
def get_image(imei, name: 'Name of the image'):
    """
    Get Image By Name
    Returns the image file with the given name if it exists.
    """
    try:
        return image_database.get_image_data(imei, name)
    except FileNotFoundError:
        return '', 400


@cubesat.post('/command')
@authenticate(token_auth)
@body(CommandUplinkSchema)
@response(CommandResponseSchema)
def uplink_command(uplink):
    """
    Uplink Command
    Process a command to be sent to the CubeSat via the RockBlock portal.
    Opcode, namespace, field, and value fields must be valid per the Alpha flight SW documentation.
    """
    print(uplink)
    uplink_response = control_protocol.handle_command(uplink['imei'], uplink['commands'])
    api_response = {
        'status': 'success' if uplink_response.find("OK") != -1 else 'failure',
        'timestamp': time.time() * 1000,
        'imei': uplink['imei'],
        'commands': uplink['commands'],
        'message': uplink_response
    }

    # log commands
    with open(f"{config.cmd_log_root_dir}/{uplink['imei']}.txt", 'a') as f:
        f.write(json.dumps(api_response) + '\n')

    return api_response


@cubesat.get('/command_data')
@authenticate(token_auth)
def get_command_meta():
    """
    Get Command Metadata
    Get list of all SFR and Fault namespaces and fields along with their metadata
    such as their type, minimum value, or maximum value.
    """
    return {
        "SFR_Override": SFR_OVERRIDE_OPCODES_MAP,
        "Faults": FAULT_OPCODE_MAP
    }


@cubesat.get('/command_history/<imei>')
@authenticate(token_auth)
@response(CommandResponseSchema(many=True))
def get_command_history(imei):
    """
    Get Command History
    Get all previously sent commands to the CubeSat via the RockBlock portal.
    """
    
    history = []
    if not exists(f"{config.cmd_log_root_dir}/{imei}.txt"):
            return []
    with open(f"{config.cmd_log_root_dir}/{imei}.txt") as f:
            for entry in f.readlines():
                history.append(json.loads(entry[:-1]))

    history.reverse()
    return history


@cubesat.get('/processed_commands/<imei>')
@authenticate(token_auth)
def get_processed_commands(imei):
    """
    Get Processed Commands
    Get previously sent commands to the CubeSat via the Rockblock portal
    that have been confirmed in the command log of the normal report. Only 
    retrieves command logs in normal reports that have timestamps after the
    timestamp of the first command sent. 
    """

    epoch = 0
    with open(f"{config.cmd_log_root_dir}/{imei}.txt") as file:
        first_line = file.readline()
        if first_line:
            first_entry = json.loads(first_line.strip())
            epoch = first_entry.get('timestamp')
        else:
            print("Error: The file is empty (no commands sent)")
    first_timestamp = datetime.datetime.utcfromtimestamp(int(epoch) / 1000).isoformat()
    # print(first_timestamp)
    query = {
        "range": {
            "transmit_time": {
                "gte": first_timestamp,
                "lte": "now"
            }
        }
    }
    res = elastic.get_es_data(config.cubesat_db_index, ['imei', 'command_log'], query=query)
    print(res)
    logs = []
    for entry in res:
        if entry['imei'] == int(imei):
            logs.append(entry['command_log'])
    print(logs)
    return logs



@cubesat.get('/downlink_history')
@authenticate(token_auth)
@response(DownlinkHistorySchema(many=True))
def get_downlink_history():
    """
    Get Downlink History
    Gets transmit type, opcode, and error message of all downlinks previously processed
    by the ground station
    """
    # https://www.elastic.co/guide/en/elasticsearch/reference/current/query-dsl-range-query.html
    return elastic.get_es_data(config.rockblock_db_index,
                               ['imei', 'telemetry_report_type', 'transmit_time', 'error', 'normal_report_id'],
                               sort=[{"transmit_time": {"order": "desc"}}])
