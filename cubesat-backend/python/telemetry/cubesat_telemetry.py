import traceback
from enum import Enum

import config
import databases.elasticsearch as es
import databases.image_database as img
import telemetry.rockblock_telemetry as rb
import util.binary.hex_string as hex
from util.binary.binary_parser import BinaryParser


class Opcodes(int, Enum):
    """Packet Opcodes for cubesat (see Alpha documentation for specification)"""

    normal_report = 99
    deployment_report = 24
    ttl = 42
    empty_packet = 0
    error = -1

# list of different fragment numbers received
fragment_list = []
# keeps track of various stats regarding the imu received imu fragments
imu_display_info = {'latest_fragment': 0,
                    'missing_fragments': [],
                    'highest_fragment': 0}

def save_cubesat_data(data: dict):
    """
    Saves a cubesat report to elasticsearch \n
    :param data: fully processed normal report
    """
    es.index(config.cubesat_db_index, es.daily_index_strategy, data)

def map_range(x, in_min, in_max, out_min, out_max):
    """
    Recreation of Arduino map() function used in flight code
    https://www.arduino.cc/reference/en/language/functions/math/map/

    :param x: the number to map
    :param in_min: the lower bound of the value’s current range
    :param in_max: the upper bound of the value’s current range
    :param out_min: the lower bound of the value’s target range
    :param out_max: the upper bound of the value’s target range
    :return: the mapped value
    """
    return out_min + (((out_max - out_min) / (in_max - in_min)) * (x - in_min))

def generate_missing_fragments(frag_list: list):
    """
    Finds the missing fragments and the highest fragment received for IMU deployment downlinks.
    Counts through all already-received fragments every time because fragments could be received in random order.

    :param frag_list: list of previously received fragments
    """
    max_frag = max(frag_list)
    imu_display_info['missing_fragments'] = []
    imu_display_info['highest_fragment'] = max_frag
    for x in range(max_frag):
        if frag_list.count(x) == 0:
            imu_display_info['missing_fragments'].append(x)

def compute_cycle_values(x_gyro, y_gyro, z_gyro) -> dict:
    """
    Maps imu cycle values from the range used for transmission (0 - 255) to their actual range (-180 - 180) \n
    :return: dictionary with normalized imu values
    """
    return {
        'x_gyro': map_range(float(x_gyro), 0, 255, -180, 180),
        'y_gyro': map_range(float(y_gyro), 0, 255, -180, 180),
        'z_gyro': map_range(float(z_gyro), 0, 255, -180, 180)
    }

def save_cycle_report(cycle_data: dict):
    """
    Saves a cycle report to elasticsearch \n
    :param cycle_data: fully processed imu cycle report
    """
    es.index(config.cycle_db_index, es.daily_index_strategy, cycle_data)

def separate_cycles(fragment_number: int, fragment_data: str):
    """
    Decodes imu cycles to retrieve the x, y, and z gyro values for each and saves them to elasticsearch \n
    :param fragment_number: id number of fragment
    :param fragment_data: hex string containing the packet's imu cycle data
    """
    for x in range(0, len(fragment_data), 6):
        x_gyro = int(fragment_data[x:x+2], 16)
        y_gyro = int(fragment_data[x+2:x+4], 16)
        z_gyro = int(fragment_data[x+4:x+6], 16)
        # every full fragment has 22 cycles, new cycle occurs every six digits in the hex string
        cycle_count = fragment_number * 22 + x / 6

        report_data = {
            'cycle_count': int(cycle_count),
            **compute_cycle_values(x_gyro, y_gyro, z_gyro)
        }
        print('report', report_data)
        save_cycle_report(report_data)

def save_deploy_report(data: dict):
    """
    Saves a deployment report to elasticsearch \n
    :param data: imu fragment summary report (latest, missing, and highest received fragments)
    """
    es.index(config.deploy_db_index, es.daily_index_strategy, data)

def process_deploy_data(data: dict):
    """
    Generates missing imu fragments, processes imu cycles, and saves fragment stats to elasticsearch \n
    :param data: dictionary with imu fragment data
    """
    fragment_list.append(data['fragment_number'])
    imu_display_info['latest_fragment'] = data['fragment_number']
    generate_missing_fragments(fragment_list)
    print(fragment_list, imu_display_info)
    separate_cycles(data['fragment_number'], data['fragment_data'])
    save_deploy_report({**report_metadata(data), **imu_display_info})

def save_image_data(data: dict):
    """
    Saves an image fragment report to elasticsearch \n
    :param data: processed image fragment report
    """
    es.index(config.image_db_index, es.daily_index_strategy, data)

def process_ttl_data(data: dict):
    """
    Process image fragment data sent by cubesat. Image comes over several fragments as
    rockblock only supports so much protocol. Image 'fragments' are then assembled into full images
    when fully collected, and saved into the image database

    :param data: image fragment report
    """
    img.save_fragment(data['serial_number'], data['fragment_number'], data['fragment_data'])
    img.try_save_image(data['serial_number'], data['max_fragments'])
    save_image_data({**report_metadata(data), **img.get_img_display_info()})

def read_opcode(parser: BinaryParser) -> Opcodes:
    """
    Reads the opcode of an incoming packet. If empty packet is received, returns Opcodes.empty_packet instead.

    :param parser: BinaryParser object constructed with the packet's data
    :return: opcode of the packet
    """
    if parser.remaining() == 0:
        return Opcodes.empty_packet
    else:
        return Opcodes(parser.read_uint8())

def read_img_hex_fragment(data: str) -> dict:
    """
    Reads the hexadecimal string of an image fragment to determine if the
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
          - The serial number is stored in the indices of [0, 2) of the hex string.
          - The fragment number is stored in the indices [8, 10) of the hex string.
            Fragment count starts at 0.
          - The fragment data starts at index 10 and goes to the end of the hex string
            or to the end of end-marker 'ffd9'.
          - The entire hex string for an image fragment data is 69 bytes long (138 characters).

    :param data: hex string containing image fragment data
    :return: a dictionary with the fragment's serial #, id #, data and the total # of fragments
    """

    serial_number = int(data[0:2], 16)
    fragment_number = int(data[8:10], 16)
    end_marker_present = data.count('ffd9') != 0
    end_marker_index = data.index('ffd9') if end_marker_present else -1
    max_fragments = fragment_number + 1 if end_marker_present else -1
    end_boundary = end_marker_index + 4 if end_marker_present else 138
    fragment_data = hex.hex_str_to_bytes(data[10:end_boundary])
    return {
        'serial_number': serial_number,
        'fragment_number': fragment_number,
        'max_fragments': max_fragments,
        'fragment_data': fragment_data
    }

def computer_normal_report_values(data: dict) -> dict:
    """
    Maps normal report values from the range used for transmission (0 - 255) to their actual range (see spec) \n
    :param data: decoded normal report
    :return: fully processed normal report
    """
    fixed_data = {
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
    data.update(fixed_data)
    return data

def read_imu_hex_fragment(data: str) -> dict:
    """
    Separates the fragment's id number and data and returns them in a dictionary, where
    "fragment_number" is the id number of the fragment and "fragment_data" is the hex string
    downlinked from the IMU, which includes the fragment number and the x, y, and z gyro values

    :param data: hex string containing imu fragment data
    :return: a dictionary with the fragment's id number and data
    """
    return {
        'fragment_number': int(data[0:2], 16),
        'fragment_data': data[2:]
    }

def read_packet_data(opcode: Opcodes, data: str='', parser: BinaryParser=None):
    """
    Reads data from a packet based on opcode.
    Note: Image data is received in fragments, which must be assembled into a full image after
    receiving all fragments. The serial number is which image is being sent, and the fragment number
    is which part of the image being sent.

    :param opcode: opcode of packet
    :param data: data hex string with opcode removed, required argument for deploy + image reports
    :param parser: BinaryParser object constructed with the packet's data, required argument for normal reports
    :return: processed/decoded normal, deploy, or image report
    """

    if opcode == Opcodes.normal_report:
        return computer_normal_report_values(parser.read_structure(config.normal_report_structure))
    elif opcode == Opcodes.deployment_report:
        return read_imu_hex_fragment(data)
    elif opcode == Opcodes.ttl:
        return read_img_hex_fragment(data)

def report_metadata(rockblock_report: dict) -> dict:
    """
    Returns rockblock metadata such as imei and transmit time from a rockblock report as a dictionary.

    :param rockblock_report: raw data report from rockblock API
    :return: map containing the report's imei and transmit time
    """
    return {
        'imei': rockblock_report['imei'],
        'transmit_time': rockblock_report['transmit_time']
    }

def error_data(rockblock_report: dict, error_msg: str) -> dict:
    """
    Returns a map containing a cubesat report with the error opcode, raw data, and an error message.

    :param rockblock_report: raw data report from rockblock API
    :param error_msg: the error messsage
    :return: an error report
    """
    return {
        'telemetry_report_type': Opcodes.error,
        'error': error_msg,
        'raw_data': rockblock_report['data']
    }

def read_cubesat_data(rockblock_report: dict) -> dict:
    """
    Reads the cubesat data inside a rockblock report. Returns a map containing the data if read,
    or an error report if the packet is empty or some issue occurred. If the data is successfully read,
    the opcode is returned in the result map under the key "telemetry_report_type". Otherwise, the
    "telemetry_report_type" key is set to Opcodes.error

    :param rockblock_report: raw data report from rockblock API
    :return: processed/decoded rockblock report or error report if empty or exception occurred
    """

    binary_data = rb.get_cubesat_message_binary(rockblock_report)
    parser = BinaryParser(binary_data)
    opcode = read_opcode(parser)
    data = rockblock_report['data'][2:] # strip opcode from cubesat data hex string

    if opcode == Opcodes.empty_packet:
        result = error_data(rockblock_report, 'empty packet')
    else:
        try:
            if opcode == Opcodes.normal_report:
                result = read_packet_data(opcode, parser=parser)
            else: # deployment and image reports
                result = read_packet_data(opcode, data=data)
            result['telemetry_report_type'] = opcode
        except Exception:
            result = error_data(rockblock_report, traceback.format_exc())
    return {**report_metadata(rockblock_report), **result}