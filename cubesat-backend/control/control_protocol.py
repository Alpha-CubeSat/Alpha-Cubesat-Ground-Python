#TODO: Import requirements
import requests
import json

# CONSTANTS
ROCKBLOCK_ENDPOINT = 'https://core.rock7.com/rockblock/MT'
UPLINK_OPCODES =  {
    'burnwire_burn_time': '0300',
    'burnwire_arm_time': '0400',
    'rockblock_downlink_period': '0500',
    'request_img_fragment': '0600'
}
ARG_LENGTH = 8
# CONSTANTS


"""Translates decimal number n into an all uppercase hexidecimal string without '0x' header.

Then pads hexadecimal string with with '0's at the beginning until it is length n,
then flips it so that it is in the format of a command argument.

Example:
format_arg(340) # 340 in decimal is 154 in hex
340 -> 154-> '00000154' (or 00 00 01 54) -> '54010000' (or 54 01 00 00)"""
def format_arg(n):
    hex_string = (hex(n)[2:]).upper()
    while len(hex_string) < ARG_LENGTH:
        hex_string = "0" + hex_string

    flipped_hex_string = ""
    for i in range(len(hex_string) - 2, -1, -2):
        flipped_hex_string += hex_string[i:i + 2]
    return flipped_hex_string

"""Takes a Command and translates it to a string representation as
specified in the Alpha documentation

The command is a dictionary with the form {'operation': <operation>, 'arg1': <arg1>}
The <operation> value must be a string key in the uplink_opcodes dictionary.
Example:
command = {'operation': 'burnwire_burn_time', 'arg1': 3, 'arg2': 0}
parse_single_arg(command) returns the string '03000300000000000000' 
or ('0300' + '03000000' + '00000000')."""
def parse_command(command):
    opcode = UPLINK_OPCODES[command['operation']]
    arg1 = format_arg(command['arg1'])
    arg2 = format_arg(command['arg2'])
    return opcode+ arg1 + arg2


"""Sends an uplink request to the satellite via the
Rockblock API. Requires rockblock user, password, and
imei for the radio, as well as the string data to send. Returns
the rockblock web services response data as a map with keys [:status :id :error-code :description].
:description and :code are only returned when there is an error, and :id is only returned on success
The possible responses are documented at https://www.rock7.com/downloads/RockBLOCK-Web-Services-User-Guide.pdf"""
def send_uplink(imei, user, password, data):
    request = {
        'imei': imei,
        'user': user,
        'password': password,
        'data': data,
        }

    response = requests.post(ROCKBLOCK_ENDPOINT, json = request)
    print(response.text + "\n")
