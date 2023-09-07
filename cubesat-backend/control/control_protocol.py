import json
from datetime import datetime

import requests

from config import *


def format_arg(n):
    """
    Helper function that translates the decimal number n into an all uppercase
    hexadecimal string without '0x' header, then pads hexadecimal string with '0's
    at the beginning until it has the length of ARG_LENGTH.
    """
    arg = (hex(int(n))[2:]).upper()
    while len(arg) < ARG_LENGTH:
        arg = "0" + arg
    return arg

def format_flag(n):
    """
    Helper function that translates the decimal number n into an all uppercase
    hexadecimal string without '0x' header, then pads hexadecimal string with '0's
    at the beginning until it has the length of FLAG_LENGTH.
    """
    flag = (hex(n)[2:]).upper()
    while len(flag) < FLAG_LENGTH:
        flag = "0" + flag
    return flag

def parse_command(command):
    """
    Takes a Command and translates it to a string representation as
    specified in the Alpha documentation
    """
    selected_opcode = command['opcode']
    if selected_opcode == 'SFR_Override':
        namespace = command['namespace']
        field = command['field']
        value = command['value']
        opcode = SFR_OVERRIDE_OPCODES_MAP[namespace][field]
        arg1 = format_arg(int(value))
        arg2 = format_arg(0)
    else:
        opcode = BURNWIRE_OPCODES[selected_opcode]
        arg1 = format_arg(0)
        arg2 = format_arg(0)
    return opcode + arg1 + arg2

def log_command(command):
    """
    Stores the result of uplinking a command into the command text file logs.
    """
    currentMinute = datetime.now().minute
    currentHour = datetime.now().hour
    currentDay = datetime.now().day
    currentMonth = datetime.now().month
    currentYear = datetime.now().year

    time = str(currentHour) + ":" + str(currentMinute)
    date = str(currentMonth) + "/" + str(currentDay) + "/" + str(currentYear)
    writeContent = f"{date},{time},{json.dumps(command)}\n"
    filename = f"commands_{currentYear}.txt"
    file = open(filename, 'a')
    file.write(writeContent)
    file.close()

    # TODO: Add RockBlock response and status of the command

def handle_command(commands):
    """
    Handles a list of commands created by a ground system to send to
    the satellite. Authenticates with rockblock web services using credentials
    provided in the config file
    """
    print("Processing commands!")
    uplink = ""
    for command in commands:
        log_command(command)
        uplink += parse_command(command)

    uplink += format_flag(0) + format_flag(250)
    return send_uplink(uplink)

def send_uplink(data):
    """
    Sends an uplink request to the satellite via the Rockblock API.
    Requires the string data to uplink.
    Returns the rockblock web services response data as a map with keys [:status :id :error-code :description].
    :description and :code are only returned when there is an error, and :id is only returned on success
    The possible responses are documented at https://www.rock7.com/downloads/RockBLOCK-Web-Services-User-Guide.pdf
    """
    request = {
        "imei": rockblock_config['imei'],
        "username": rockblock_config['user'],
        "password": rockblock_config['password'],
        "data": data,
    }
    print(request)

    response = requests.post(ROCKBLOCK_ENDPOINT, data = request)
    print(response.text + "\n")
    return response.text
