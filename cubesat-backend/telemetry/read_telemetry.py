from telemetry.binary_parser import BinaryParser
from telemetry.telemetry_constants import *

uint8_max = pow(2, 8) - 1
uint16_max = pow(2, 16) - 1
uint32_max = pow(2, 32) - 1


def map_range(x, out_min, out_max, in_min=0, in_max=255):
    """
    Recreation of Arduino map() function used in flight code
    https://www.arduino.cc/reference/en/language/functions/math/map/
    """
    return out_min + (((out_max - out_min) / (in_max - in_min)) * (x - in_min))


def compute_normal_report_values(data: dict) -> dict:
    """
    Maps normal report values from the range used for transmission (0 - 255) to their actual range (see spec) \n
    :param data: decoded normal report
    :return: fully processed normal report
    """
    fixed_data = {
        'boot_time_mins': map_range(float(data['boot_time_mins']), 0, uint8_max),
        'burn_time': map_range(float(data['burn_time']), 0, 5000),
        'armed_time': map_range(float(data['armed_time']), 0, 43200000),
        'lp_downlink_period': map_range(float(data['lp_downlink_period']), 1000, 172800000),
        'transmit_downlink_period': map_range(float(data['transmit_downlink_period']), 1000, 172800000),
        'acs_mode' : map_range(float(data['acs_mode']), 0, uint8_max),
        'Id_index': map_range(float(data['Id_index']), 0, 0),
        'Kd_index': map_range(float(data['Kd_index']), 0, 0),
        'Kp_index': map_range(float(data['Kp_index']), 0, 0),
        'c_index': map_range(float(data['c_index']), 0, 0),
        'boot_counter': map_range(float(data['boot_counter']), 0, uint8_max),
        'dynamic_data_addr': map_range(float(data['dynamic_data_addr']), 10, 459),
        'sfr_data_addr': map_range(float(data['sfr_data_addr']), 460, 4085),
        'time_alive': map_range(float(data['time_alive']), 0, uint32_max),
        'dynamic_data_age': map_range(float(data['dynamic_data_age']), 0, uint32_max),
        'sfr_data_age': map_range(float(data['sfr_data_age']), 0, uint32_max),
        'acs_on_time': map_range(float(data['acs_on_time']), 0, 5400000),
        'rockblock_on_time': map_range(float(data['rockblock_on_time']), 0, 5400000),
        'light_val_average_standby': map_range(float(data['light_val_average_standby']), 0, 1023),
        'mag_x_average': map_range(float(data['mag_x_average']), -150, 150),
        'mag_y_average': map_range(float(data['mag_y_average']), -150, 150),
        'mag_z_average': map_range(float(data['mag_z_average']), -150, 150),
        'gyro_x_average': map_range(float(data['gyro_x_average']), -5, 5),
        'gyro_y_average': map_range(float(data['gyro_y_average']), -5, 5),
        'gyro_z_average': map_range(float(data['gyro_z_average']), -5, 5),
        'temp_c_value': map_range(float(data['temp_c_value']), -100, 200),
        'temp_c_average': map_range(float(data['temp_c_average']), -100, 200),
        'solar_current_average': map_range(float(data['solar_current_average']), -75, 500),
        'voltage_value': map_range(float(data['voltage_value']), 0, 6),
        'voltage_average': map_range(float(data['voltage_average']), 0, 6),
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
        'fragment_data': data[2:] if not end_flag_present else data[2:data.index('fe92')],
        'end_flag_present': end_flag_present
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
    max_fragments = fragment_number + 1 if end_marker_present else -1
    fragment_data = bytearray.fromhex(
        data[10:] if not end_marker_present else data[10:data.index('ffd9')])
    return {
        'serial_number': int(data[0:2], 16),
        'fragment_number': fragment_number,
        'max_fragments': max_fragments,
        'fragment_data': fragment_data
    }


def error_data(error_msg: str) -> dict:
    """
    Returns a map containing a cubesat report with the error opcode and the error message.
    """
    return {
        'telemetry_report_type': Opcodes.error,
        'error': error_msg
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

    parser = BinaryParser(binary_data)
    if parser.remaining() == 0:
        return error_data('Empty packet')
    else:
        opcode_val = parser.read_uint8()
        if opcode_val in list(map(int, Opcodes)):
            opcode = Opcodes(opcode_val)
        else:
            return error_data('Invalid opcode: ' + str(opcode_val))

    # Extract data from report (strip away opcode [0:2])
    data = rockblock_report['data'][2:]

    # Reads data from a packet based on its opcode
    if opcode == Opcodes.normal_report:
        result = compute_normal_report_values(
            parser.read_structure(normal_report_structure))
        # print(result)
    elif opcode == Opcodes.imu_report:
        result = read_imu_hex_fragment(data)
    elif opcode == Opcodes.camera_report:
        result = read_img_hex_fragment(data)
    result['telemetry_report_type'] = opcode
    return result
