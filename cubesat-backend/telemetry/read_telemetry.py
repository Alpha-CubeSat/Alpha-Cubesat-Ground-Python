import traceback

from telemetry.telemetry_constants import *
from util.binary_parser import BinaryParser


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

def compute_normal_report_values(data: dict) -> dict:
    """
    Maps normal report values from the range used for transmission (0 - 255) to their actual range (see spec) \n
    :param data: decoded normal report
    :return: fully processed normal report
    """
    fixed_data = {
        'burnwire_burn_time': map_range(float(data['burnwire_burn_time']), 0, 255, 0, 5000),
        'burnwire_armed_timeout_limit': map_range(float(data['burnwire_armed_timeout_limit']), 0, 255, 0, 864000000),
        # 'burnwire_attempts': map_range(float(data['burnwire_attempts']), 0, 255, 0, 10),
        'downlink_period': map_range(float(data['downlink_period']), 0, 255, 60000, 172800000),
        'x_mag': map_range(float(data['x_mag']), 0, 255, -150, 150),
        'y_mag': map_range(float(data['y_mag']), 0, 255, -150, 150),
        'z_mag': map_range(float(data['z_mag']), 0, 255, -150, 150),
        'x_gyro': map_range(float(data['x_gyro']), 0, 255, -5, 5),
        'y_gyro': map_range(float(data['y_gyro']), 0, 255, -5, 5),
        'z_gyro': map_range(float(data['z_gyro']), 0, 255, -5, 5),
        'photoresistor' : map_range(float(data['photoresistor']), 0, 255, 0, 1023),
        'temp': map_range(float(data['temp']), 0, 255, -50, 200),
        # 'solar_current': map_range(float(data['solar_current']), 0, 255, 0, 500),
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
    end_flag_present = data.count('fe92') != 0
    return {
        'fragment_number': int(data[0:2], 16),
        'fragment_data': data[2:] if not end_flag_present else data[2:data.index('fe92')]
    }


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

    fragment_number = int(data[8:10], 16)
    end_marker_present = data.count('ffd9') != 0
    end_marker_index = data.index('ffd9') if end_marker_present else -1
    max_fragments = fragment_number + 1 if end_marker_present else -1
    end_boundary = end_marker_index + 4 if end_marker_present else 138
    fragment_data = bytearray.fromhex(data[10:end_boundary])
    return {
        'serial_number': int(data[0:2], 16),
        'fragment_number': fragment_number,
        'max_fragments': max_fragments,
        'fragment_data': fragment_data
    }



def error_data(rockblock_report: dict, error_msg: str) -> dict:
    """
    Returns a map containing a cubesat report with the error opcode, raw data, and an error message.

    :param rockblock_report: raw data report from rockblock API
    :param error_msg: the error message
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
    # Convert hex encoded data into a python byte array
    binary_data = bytearray.fromhex(rockblock_report['data'])

    # Read opcode of report
    parser = BinaryParser(binary_data)
    if parser.remaining() == 0:
        opcode = Opcodes.empty_packet
    else:
        opcode = Opcodes(parser.read_uint8())

    # Extract data from report (strip away opcode [0:2])
    data = rockblock_report['data'][2:]
    # Reads data from a packet based on its opcode
    if opcode == Opcodes.empty_packet:
        return error_data(rockblock_report, 'empty packet')
    else:
        try:
            if opcode == Opcodes.normal_report:
                result = compute_normal_report_values(
                    parser.read_structure(normal_report_structure))
                print(result)
            elif opcode == Opcodes.imu_report:
                result = read_imu_hex_fragment(data)
            else:  # opcode == camera_report
                result = read_img_hex_fragment(data)
            result['telemetry_report_type'] = opcode
            return result
        except Exception:
            return error_data(rockblock_report, traceback.format_exc())