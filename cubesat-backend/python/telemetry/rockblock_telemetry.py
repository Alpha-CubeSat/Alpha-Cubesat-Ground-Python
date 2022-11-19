import traceback

import jwt
import pem

import config
import databases.elasticsearch as es
import util.binary.byte_buffer as buffer
import util.binary.hex_string as hex


# s/defschema RockblockReport ??????

# "Public key provided for JWT verification by rockblock web services documentation"
def rockblock_web_pk():
    return pem.parse_file('cert.pem')

# "Uses jwt to verify data sent by rockblock web services. Returns a copy of the data if valid,
#   nil if invalid/corrupt"
def verify_rockblock_request(rockblock_report):
    try:
        jwt_data = rockblock_report['JWT']
        unsigned_data = jwt.decode(jwt_data, rockblock_web_pk(), algorithms=['rs256'])
        unsigned_data['JWT'] = jwt_data # ????
    except:
        traceback.print_exc()

# "Gets the string encoded binary data sent by the cubesat as a java nio ByteBuffer"
def get_cubesat_message_binary(rockblock_report):
    return buffer.from_byte_array(hex.hex_str_to_bytes(rockblock_report['data']))

#   "Saves a rockblock report to elasticsearch. Gets latitude and longitude
#    data and makes a single field out of them"
def save_rockblock_report(data):
    location = {
        'lat': data['iridium_latitude'],
        'lon': data['iridium_longitude']
    }
    data['location'] = location
    index = config.rockblock_db_index
    es.index(index, es.daily_index_strategy, data)

#   "Convert Rockblock's nonstandard date format to YYYY-MM-DDThh:mm:ssZ.
#   Rockblock uses YY-MM-DD HH:mm:ss as the date format, despite their documentation claiming to use a more standard
#   format: YYYY-MM-DDThh:mm:ssZ. Conversion is done by appending '20' to the start of the date string,
#   which means this fix may not work after the year 2100."
def fix_rb_datetime(dt):
    return f"20{dt.replace(' ', 'T')}Z"