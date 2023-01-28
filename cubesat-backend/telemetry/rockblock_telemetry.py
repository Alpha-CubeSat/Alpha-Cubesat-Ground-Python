import os

import jwt
import pem

import config
import databases.elastic_search as es
import util.binary.hex_string as hex


def get_cubesat_message_binary(rockblock_report: dict) -> bytearray:
    """
    Converts the hex encoded data sent by the cubesat into a python byte array
    :param rockblock_report: raw data report from rockblock API
    :return: byte array representation of the rockblock report's "data" attribute
    """
    return hex.hex_str_to_bytes(rockblock_report['data'])

def save_rockblock_report(data: dict):
    """
    Saves a rockblock report to elasticsearch. Combines latitude and longitude into a single field. \n
    :param data: raw data report from rockblock API
    """
    data['location'] = {
        'lat': data['iridium_latitude'],
        'lon': data['iridium_longitude']
    }
    es.index(config.rockblock_db_index, es.daily_index_strategy, data)

# Public key provided for JWT verification by rockblock web services documentation
rockblock_web_pk = pem.parse_file(os.path.join(config.basedir, 'cert.pem'))

# Uses JWT to verify data sent by rockblock web services, throws exception if JWT is invalid
def verify_rockblock_request(jwt_data):
    jwt.decode(jwt_data, rockblock_web_pk, algorithms=['rs256'])

# Convert Rockblock's nonstandard date format to YYYY-MM-DDThh:mm:ssZ.
# Rockblock uses YY-MM-DD HH:mm:ss as the date format, despite their documentation claiming to use a more standard
# format: YYYY-MM-DDThh:mm:ssZ. Conversion is done by appending "20" to the start of the date string,
# which means this fix may not work after the year 2100.
def fix_rockbock_datetime(datetime):
    print('raw dt:', datetime)
    fixed = f"20{datetime.replace(' ', 'T')}Z"
    print('fixed dt:', datetime)
    return fixed