#TODO: Import requirements

rockblock_endpoint = 'https://core.rock7.com/rockblock/MT'
uplink_opcodes =  {
    'burnwire_burn_time': '0300',
    'burnwire_arm_time': '0400',
    'rockblock_downlink_period': '0500',
    'request_img_fragment': '0600'
}

"""Pads hex_string with with '0's at the beginning until it is length n,
then flips it so that it is in the format of a command argument.

Example:
pad_hex_string()
'00000154' (or 00 00 01 54) -> '54010000' (or 54 01 00 00)"""
def pad_hex_string(hex_string, n):
    while len(hex_string) < n:
        hex_string += "0"

    new_hex_string = ""
    for i in range(len(hex_string) - 2, -1, -2):
        new_hex_string += hex_string[i]
    return new_hex_string
"""Translates decimal number n into an all uppercase hexidecimal string without '0x' header."""
def hexify_arg(n):
    return (hex(n)[2:]).upper()

"""A helper function that returns the string representation for a single
argument operation.
The operation is a dictionary with the form {'opcode': <opcode>, 'arg1': <arg1>}
The <opcode> value must be a string key in the uplink_opcodes dictionary.
Example:
operation = {'opcode': 'burnwire_burn_time', 'arg1': 3}
parse_single_arg(operation) returns the string '03000300000000000000' 
or ('0300' + '03000000' + '00000000')."""
def parse_single_arg(operation):
    return operation['opcode'] + operation['arg1']

def parse_double_arg(operation, key1, key2):
    pass

"""Takes a Command and translates it to a string representation as
specified in the Alpha documentation"""
def parse_command_args(operation):
    pass

"""Sends an uplink request to the satellite via the
Rockblock API. Requires rockblock user, password, and
imei for the radio, as well as the string data to send. Returns
the rockblock web services response data as a map with keys [:status :id :error-code :description].
:description and :code are only returned when there is an error, and :id is only returned on success
The possible responses are documented at https://www.rock7.com/downloads/RockBLOCK-Web-Services-User-Guide.pdf"""
def send_uplink(imei, user, password, data):
    pass