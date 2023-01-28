import base64

def hexify(s: str) -> str:
    """Returns hex representation of the input string"""
    return s.encode('utf-8').hex()

def unhexify(hex_str: str) -> str:
    """Returns a string containing the results of decoding a hex string"""
    return bytes.fromhex(hex_str).decode('utf-8')

def hex_str_to_bytes(hex_str: str) -> bytearray:
    """Returns byte array representation of a hex string"""
    return bytearray.fromhex(hex_str)

def bytes_to_b64(bytes: bytes) -> bytes:
    """Returns base64 representation of bytes"""
    return base64.b64encode(bytes)
