
rockblock_endpoint = 'https://core.rock7.com/rockblock/MT'
uplink_opcodes =  {
    'burnwire_burn_time': '0300',
    'burnwire_arm_time': '0400',
    'rockblock_downlink_period': '0500',
    'request_img_fragment': '0600'
}

"""Flips a hexadecimal sequence of 4 bytes so that it is ready to submitted as
a command argument.
Example:
'00000154' (or 00 00 01 54) -> '54010000' (or 54 01 00 00)"""
def flip_bytes(hex_string):
    pass

"Pads a hex string with with '0's at the beginning until it is length 8."
def pad_hex_string(s):
    pass

"Translates decimal number into a hexidecimal string."
def hexify_arg(s):
    pass

"""A helper function that returns the string representation for a single
argument operation
Example:
(parse-single-arg {:type :burnwire-burn-time :example 3} :example)
returns the string '03000300000000000000' ('0300' + '03000000' + '00000000')"""
def parse_single_arg(operation, key):
    pass

def parse_double_arg(operation, ley1, key2):
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