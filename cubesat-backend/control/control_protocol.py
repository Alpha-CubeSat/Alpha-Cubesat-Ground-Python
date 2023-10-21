import requests

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

def format_sfr_args(args : dict) -> (int,int):
    """
    Helper function that translates dictionary values into all uppercase 
    hexadecimal string without the '0x' header. The string is passed in order
    of the dictionary keys; there must be a key 'byteCount' that specifies the 
    size of each of the dictionary values.
    """
    arg1 = ""
    arg2 = ""
    value = args["value"]
    if value in ['true', 'false']:
        value = bool(value)
    arg1 += format_single_arg(int(value), ARG_LENGTH)
    arg2 += format_single_arg(int(args["setValue"] == True), 2)
    arg2 += format_single_arg(int(args["setRestore"] == True), 2)
    arg2 += format_single_arg(int(args["restoreValue"] == "true"), 4)
    return arg1, arg2

def format_eeprom_args(args : dict) -> (int, int):
    """
    Helper function that translates dictionary values into all uppercase 
    hexadecimal string without the '0x' header. The string is passed in order
    of the dictionary keys; there must be a key 'byteCount' that specifies the 
    size of each of the dictionary values.
    """
    pass

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
    if selected_opcode == 'SFR_Override':
        namespace = command['namespace']
        field = command['field']
        value = command['value']
        arg1, arg2 = format_sfr_args(value)
        opcode = SFR_OVERRIDE_OPCODES_MAP[namespace][field]['hex']
    elif selected_opcode == 'EEPROM_Reset':
        arg1, arg2 = format_eeprom_args(value)
        opcode = EEPROM_RESET_OPCODE
    else:
        opcode = BURNWIRE_OPCODES[selected_opcode]
        arg1 = format_single_arg(0, ARG_LENGTH)
        arg2 = format_single_arg(0, ARG_LENGTH)
    print(opcode + arg1 + arg2)
    return opcode + arg1 + arg2

def handle_command(imei: str, commands: list) -> str:
    """
    Handles a list of commands created by a ground system to send to
    the satellite. Authenticates with rockblock web services using credentials
    provided in the config file
    """
    print("Processing commands!")
    uplink = ""
    for command in commands:
        uplink += parse_command(command)

    uplink += format_flag(0) + format_flag(250)
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

    response = requests.post(ROCKBLOCK_ENDPOINT, data = request)
    print(response.text + "\n")
    return response.text
