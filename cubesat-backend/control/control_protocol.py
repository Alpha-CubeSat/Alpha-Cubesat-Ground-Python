import math

import requests

from api.errors import failure_response
from config import rockblock_config
from control.control_constants import *


def format_single_arg(n: int, arg_length) -> str:
    """
    Helper function that translates the decimal number n into an all uppercase
    hexadecimal string without '0x' header, then pads hexadecimal string with '0's
    at the beginning until it has the length of ARG_LENGTH.
    """
    arg = (hex(n)[2:]).upper()
    while len(arg) < arg_length:
        arg = "0" + arg
    return arg


def format_sfr_args(field_data: dict, args: dict) -> (int, int):
    """
    Helper function that translates sfr override dictionary values into all 
    uppercase hexadecimal string without the '0x' header. Combines the hex 
    strings into arg1 and arg2 in the format expected by flight software.
    """
    arg1, arg2, value = "", "", args["value"]
    if field_data['type'] == SFR_T.BOOL:
        if value not in ['true', 'false']:
            return failure_response('Boolean expected', 400)
        value = bool(value)
    else:
        if field_data['type'] in [SFR_T.INT, SFR_T.TIME]:
            value = int(value)
        else: # field_data['type'] == SFR_T.FLOAT
            value = int(float(value) * field_data['resolution'])

        if ((field_data.get('min') is not None and value < field_data['min']) or
                (field_data.get('max') is not None and value > field_data['max'])):
            return failure_response('Min/Max Bounds Violated', 400)

    arg1 += format_single_arg(value, ARG_LENGTH)
    arg2_parts = [
        (int(args["setValue"]), 2),
        (int(args["setRestore"]), 2),
        (int(args["restoreValue"] == "true"), 4),
    ]
    arg2 = ''.join(format_single_arg(part, length) for part, length in arg2_parts)
    return arg1, arg2


def format_eeprom_args(args: dict) -> (int, int):
    """
    Helper function that translates dictionary values into all uppercase 
    hexadecimal string without the '0x' header. The string is passed in order
    of the dictionary keys; there must be a key 'byteCount' that specifies the 
    size of each of the dictionary values.
    """
    arg1_parts = [
        [int(args["bootCount"]), 2],
        [int(args["lightSwitch"] == "true"), 2],
        [int(args["sfrAddress"]), 4]
    ]
    arg1 = ''.join(format_single_arg(part, length) for part, length in arg1_parts)
    arg2_parts = [
        # range is 0-95000 and we need to map them to 1 byte
        [math.floor(int(args["sfrWriteAge"]) / 373), 2],
        [math.floor(int(args["dataWriteAge"]) / 373), 2],
        [int(args["dataAddress"]), 4]
    ]
    arg2 = ''.join(format_single_arg(part, length) for part, length in arg2_parts)
    return arg1, arg2


def format_fault_args(args: str) -> (int, int):
    """
    Helper function that translates the fault argument "Restore", "Force", or 
    "Suppress" into the format expected by the flight code.
    """
    zero = format_single_arg(0, ARG_LENGTH)
    one = format_single_arg(1, ARG_LENGTH)
    if args == "Force":
        return one, zero
    elif args == "Suppress":
        return zero, one
    elif args == "Restore":
        return zero, zero
    else:
        failure_response(400, 'Invalid Fault Type')


def format_flag(n: int) -> str:
    """
    Helper function that translates the decimal number n into an all uppercase
    hexadecimal string without '0x' header, then pads hexadecimal string with '0's
    at the beginning until it has the length of FLAG_LENGTH.
    """
    flag = (hex(n)[2:]).upper()
    while len(flag) < FLAG_LENGTH:
        flag = "0" + flag
    return flag


def parse_command(command: dict) -> str:
    """
    Takes a Command and translates it to a string representation as
    specified in the Alpha documentation
    """
    selected_opcode = command['opcode']
    if selected_opcode in ['Deploy', 'Arm', 'Fire']:
        opcode = BURNWIRE_OPCODES[selected_opcode]
        arg1 = format_single_arg(0, ARG_LENGTH)
        arg2 = format_single_arg(0, ARG_LENGTH)

    elif selected_opcode == 'SFR_Override':
        namespace, field = command['namespace'], command['field']
        if not SFR_OVERRIDE_OPCODES_MAP.get(namespace) or not SFR_OVERRIDE_OPCODES_MAP[namespace].get(field):
            return failure_response('Invalid SFR Field', 400)
        opcode = SFR_OVERRIDE_OPCODES_MAP[namespace][field]['hex']
        arg1, arg2 = format_sfr_args(SFR_OVERRIDE_OPCODES_MAP[namespace][field], command['value'])

    elif selected_opcode == 'Fault':
        namespace, field = command['namespace'], command['field']
        if not FAULT_OPCODE_MAP.get(namespace) or not FAULT_OPCODE_MAP[namespace].get(field):
            return failure_response('Invalid Fault Field', 400)
        opcode = FAULT_OPCODE_MAP[namespace][field]['hex']
        arg1, arg2 = format_fault_args(command['value'])

    elif selected_opcode == 'Fragment_Request':
        cmd_data = command['value']
        if cmd_data['type'] == 'Capture':
            opcode = CAPTURE_REQUEST_OPCODE
            arg1 = format_single_arg(int(cmd_data['serialNum']), ARG_LENGTH)
            arg2 = format_single_arg(int(cmd_data['fragmentNum']), ARG_LENGTH)
        elif cmd_data['type'] == 'IMU':
            opcode = IMU_REQUEST_OPCODE
            arg1 = format_single_arg(int(cmd_data['fragmentNum']), ARG_LENGTH)
            arg2 = format_single_arg(0, ARG_LENGTH)
        else:
            return failure_response(400, 'Invalid Fragment Type')

    elif selected_opcode == 'EEPROM_Reset':
        arg1, arg2 = format_eeprom_args(command['value'])
        opcode = EEPROM_RESET_OPCODE

    else:
        return failure_response(400, 'Invalid Command')

    print(opcode + arg1 + arg2)
    return opcode + arg1 + arg2


def handle_command(imei: str, commands: list) -> str:
    """
    Handles a list of commands created by a ground system to send to
    the satellite. Authenticates with rockblock web services using credentials
    provided in the config file
    """
    print("Processing commands!")
    # add FEFE start flag
    uplink = format_flag(254) + format_flag(254)
    for command in commands:
        uplink += parse_command(command)

    # add FAFA end flag
    uplink += format_flag(250) + format_flag(250)
    print(uplink)
    return send_uplink(imei, uplink)

def send_uplink(imei: str, data: str) -> str:
    """
    Sends an uplink request to the satellite via the Rockblock API.
    Requires the string data to uplink.
    Returns the rockblock web services response data as a map with keys [:status :id :error-code :description].
    :description and :code are only returned when there is an error, and :id is only returned on success
    The possible responses are documented at https://www.rock7.com/downloads/RockBLOCK-Web-Services-User-Guide.pdf
    """
    request = {
        "imei": imei,
        "username": rockblock_config['username'],
        "password": rockblock_config['password'],
        "data": data,
    }

    response = requests.post(ROCKBLOCK_ENDPOINT, data=request)
    print(response.text + "\n")
    return response.text
