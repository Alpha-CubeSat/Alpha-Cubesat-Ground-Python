from enum import Enum

import config
import databases.elasticsearch as es
import databases.image_database as img
import util.binary.binary_reader as reader
import util.binary.hex_string as hex


# "Packet opcodes for cubesat (see Alpha documentation for specification)"
class opcodes(Enum):
    normal_report = 99
    deployment_report = 24
    ttl = 42

class types(Enum):
    empty_packet = 0
    error = 1

# "Saves a cubesat report to elasticsearch"
def save_cubesat_data(data):
    es.index(config.cubesat_db_index, es.daily_index_strategy, data)

# "Recreation of Arduino map() function used in flight code in order to convert imu data to correct imu values.
# https://www.arduino.cc/reference/en/language/functions/math/map/"
def map_range(x, in_min, in_max, out_min, out_max):
    return out_min + (((out_max - out_min) / (in_max - in_min)) * (x - in_min))

# fragment-number is the number of the fragment
# fragment-list is a list of different fragment numbers received
# fragment-data is the Hex String downlinked from the IMU. Includes fragment number, x-gyro values, y-gyro values, z-gyro values
# ***declared as atomic in clojure???
fragment_list = []
imu_display_info = {'latest_fragment': 0,
                    'missing_fragments': 'None',
                    'highest_fragment': 0}

# "Finds the missing fragments and the highest fragment received for IMU deployment downlinks.
# It counts through all already-received fragments every time because fragments could be received in random order."
def generate_missing_fragments(frag_list):
    max_frag = max(frag_list)
    imu_display_info['missing_fragments'] = ''
    imu_display_info['highest_fragment'] = max_frag
    for x in range(max_frag):
        if frag_list.count(x) == 0:
            imu_display_info['missing_fragments'] += str(x) + " "

    if len(imu_display_info['missing_fragments']) == 0:
        imu_display_info['missing_fragments'] = 'None'

def compute_cycle_values(x_gyro, y_gyro, z_gyro):
    return {
        'x_gyro': map_range(float(x_gyro), 0, 255, -180, 180),
        'y_gyro': map_range(float(y_gyro), 0, 255, -180, 180),
        'z_gyro': map_range(float(z_gyro), 0, 255, -180, 180)
    }

def save_cycle_report(cycle_data):
    es.index(config.cycle_db_index, es.daily_index_strategy, cycle_data)

def separate_cycles(fragment_number, fragment_data):
    for x in range(len(fragment_data)):
        x_gyro = int(fragment_data[x:x+2], 16)
        y_gyro = int(fragment_data[x+2:x+4], 16)
        z_gyro = int(fragment_data[x+4:x+6], 16)
        # every full fragment has 22 cycles, new cycle occurs every six digits in the hex string
        cycle_count = fragment_number * 22 + x / 6

        report_data = {
            **compute_cycle_values(x_gyro, y_gyro, z_gyro),
            'cycle_count': cycle_count
        }
        save_cycle_report(report_data)

def save_deploy_report(data):
    es.index(config.deploy_db_index, es.daily_index_strategy, data)

# "Saves a deployment report to elasticsearch"
def process_deploy_data(data):
    meta = {'imei': data['imei'], 'transmit_time': data['transmit_time']}
    fragment_list.append(data['fragment_number'])
    generate_missing_fragments(fragment_list)
    separate_cycles(data['fragment_number'], data['fragment_data'])
    save_deploy_report({**meta, **imu_display_info})

# "Saves an image fragment report to elasticsearch"
def save_image_data(data):
    es.index(config.image_db_index, es.daily_index_strategy, data)

# "Process image fragment data sent by cubesat. Image comes over several fragments as
# rockblock only supports so much protocol. Image 'fragments' are then assembled into full images
# when fully collected, and saved into the image database"
def process_ttl_data(data):
    meta = {'imei': data['imei'], 'transmit_time': data['transmit_time']}
    img.save_fragment(data['serial_number'], data['fragment_number'], data['fragment_data'])
    img.try_save_image(data['serial_number'], data['max_fragments'])
    save_image_data({**meta, **img.get_img_display_info()})

# "Reads the opcode of an incoming packet. If empty packet is received, returns ::empty-packet instead"
def read_opcode(packet):
    if reader.remaining(packet) == 0:
        return types.empty_packet
    else:
        return opcodes(reader.read_uint8(packet))

'''
  "Reads the hexadecimal string of an image fragment to determine if the 
   fragment is the last fragment, which is indicated by the end-marker 'ffd9'. 
   Returns the serial number in decimal form, the fragment number in 
   decimal form, the max number of fragments in decimal form, and the hex string 
   of fragment data needed to be read (minus the opcode, image serial number and 
   fragment number).
   
   If the image fragment is not last, then the max number of fragments is set 
   arbitrarily to -1, and the entirety of the fragment portion in hex string 
   must be read. If the image fragment is the last, then the max number of 
   fragments is set to (last fragment number + 1), and the hexadecimal string is 
   read up to 'ffd9'.
   
   Notes: 
          - The hex string is the data report minus the op code at the beginning
            (so everything after the op code from the downlink).
          - The serial number is stored in the indices of [0, 2) of the hex 
            string.
          - The fragment number is stored in the indices [8, 10) of the hex 
            string. Fragment count starts at 0.
          - The fragment data starts at index 10 and goes to the end of the
            hex-string or to the end of end-marker 'ffd9'.
          - The entire hex string for an image fragment data is 69 bytes long 
            (138 characters)."
'''
def read_img_hex_fragment(rockblock_data):
    serial_number = int(rockblock_data[0:2], 16)
    fragment_number = int(rockblock_data[8:10], 16)
    end_marker_present = rockblock_data.count('ffd9') != 0
    end_marker_index = rockblock_data.index('ffd9') if end_marker_present else -1
    max_fragments = fragment_number + 1 if end_marker_present else -1
    end_boundary = end_marker_index + 4 if end_marker_present else 138
    fragment_data = hex.hex_str_to_bytes(rockblock_data[10:end_boundary])
    return {
        'serial_number': serial_number,
        'fragment_number': fragment_number,
        'max_fragments': max_fragments,
        'fragment_data': fragment_data
    }

def computer_normal_report_values(data):
    return {
        'burnwire_burn_time': map_range(float(data['burnwire_burn_time']), 0, 255, 0, 60000),
        'burnwire_armed_timeout_limit': map_range(float(data['burnwire_armed_timeout_limit']), 0, 255, 0, 86400000),
        'burnwire_attempts': map_range(float(data['burnwire_attempts']), 0, 255, 0, 10),
        'downlink_period': map_range(float(data['downlink_period']), 0, 255, 1000, 172800000),
        'x_mag': map_range(float(data['x_mag']), 0, 255, -180, 180),
        'y_mag': map_range(float(data['y_mag']), 0, 255, -180, 180),
        'z_mag': map_range(float(data['z_mag']), 0, 255, -180, 180),
        'x_gyro': map_range(float(data['x_gyro']), 0, 255, -180, 180),
        'y_gyro': map_range(float(data['y_gyro']), 0, 255, -180, 180),
        'z_gyro': map_range(float(data['z_gyro']), 0, 255, -180, 180),
        'temp': map_range(float(data['temp']), 0, 255, 0, 200),
        'solar_current': map_range(float(data['solar_current']), 0, 255, 0, 500),
        'battery_voltage': map_range(float(data['battery_voltage']), 0, 255, 3, 5)
    }

def read_imu_hex_fragment(rockblock_data):
    return {
        'fragment_number': int(rockblock_data[0:2], 16),
        'fragment_data': rockblock_data[2:]
    }

'''
"Reads data from a packet based on opcode.
Note: Image data is received in fragments, :data-length bytes each, which must be assembled into a full image
after receiving all fragments. The serial number is which image is being sent, and the fragment number
is which part of the image being sent"
'''
def read_packet_data():
    pass

# "Returns rockblock metadata such as transmit time from a rockblock report as a map"
def report_metadata(rockblock_report):
    return {
        'imei': rockblock_report['imei'],
        'transmit_time': rockblock_report['transmit_time']
    }


# "Returns a map containing a cubesat report with the error opcode, raw data, and an error message"
def error_data(rockblock_report, error_msg):
    return {
        'telemetry-report-type': types.error,
        'error': error_msg,
        'raw_data': {'data': rockblock_report}
    }

'''
"Reads the cubesat data inside a rockblock report. Returns a map containing the data if read, or an error report
if the packet is empty or some issue occurred. If the data is successfully read, the opcode is returned in the
result map as :telemetry-report-type. Otherwise :telemetry-report-type is set to ::error"
'''
def read_cubesat_data(rockblock_report):
    pass