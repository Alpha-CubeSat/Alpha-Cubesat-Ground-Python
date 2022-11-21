import base64
import binascii

"Returns hex representation of the input string"
def hexify(s):
    utf = s.encode('utf-8')
    return utf.hex()

"Returns a string containing a the results of decoding a hex string"
def unhexify(hex):
    return bytes.fromhex(hex).decode('utf-8')

"Decodes a hex string into a python array of bytes"
def hex_str_to_bytes(hex_str):
    #unhex = unhexify(hex_str)
    #return bytearray(unhex, 'utf-16')
    #or
    return bytearray.fromhex(hex_str)
    # or
    #return bytearray(unhex, 'utf-8')
    # or
    #return bytearray.fromhex(hex_str)

print(hex_str_to_bytes('68656c6c6f'))

def bytes_to_b64(bytes):
    return base64.b64encode(bytes)
