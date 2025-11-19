from control.control_constants import MISSION_MODE_MAP
from telemetry.binary_parser import BinaryParser
from telemetry.telemetry_constants import *


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
        'boot_time_mins':            int(map_range(float(data['boot_time_mins']), 0, UINT8_MAX)),
        'burn_time':                 int(map_range(float(data['burn_time']), 0, 5000)),
        'armed_time':                int(map_range(float(data['armed_time']), 0, 43200000)),
        'lp_downlink_period':        int(map_range(float(data['lp_downlink_period']), 1000, 172800000)),
        'transmit_downlink_period':  int(map_range(float(data['transmit_downlink_period']), 1000, 172800000)),
        'acs_mode' :                 int(map_range(float(data['acs_mode']), 0, UINT8_MAX)),
        'Id_index':                  int(map_range(float(data['Id_index']), 0, 30)),
        'Kd_index':                  int(map_range(float(data['Kd_index']), 0, 30)),
        'Kp_index':                  int(map_range(float(data['Kp_index']), 0, 30)),
        'c_index':                   int(map_range(float(data['c_index']), 0, 30)),
        'boot_counter':              int(map_range(float(data['boot_counter']), 0, UINT8_MAX)),
        'dynamic_data_addr':         int(map_range(float(data['dynamic_data_addr']), 10, 459)),
        'sfr_data_addr':             int(map_range(float(data['sfr_data_addr']), 460, 4085)),
        'time_alive':                int(map_range(float(data['time_alive']), 0, UINT32_MAX)),
        'dynamic_data_age':          int(map_range(float(data['dynamic_data_age']), 0, UINT32_MAX)),
        'sfr_data_age':              int(map_range(float(data['sfr_data_age']), 0, UINT32_MAX)),
        'acs_on_time':               int(map_range(float(data['acs_on_time']), 0, 5400000)),
        'rockblock_on_time':         int(map_range(float(data['rockblock_on_time']), 0, 5400000)),
        'light_val_average_standby':     map_range(float(data['light_val_average_standby']), 0, 1023),
        'mag_x_average':                 map_range(float(data['mag_x_average']), -150, 150),
        'mag_y_average':                 map_range(float(data['mag_y_average']), -150, 150),
        'mag_z_average':                 map_range(float(data['mag_z_average']), -150, 150),
        'gyro_x_average':                map_range(float(data['gyro_x_average']), -10, 10),
        'gyro_y_average':                map_range(float(data['gyro_y_average']), -10, 10),
        'gyro_z_average':                map_range(float(data['gyro_z_average']), -10, 10),
        'temp_c_value':                  map_range(float(data['temp_c_value']), -100, 200),
        'temp_c_average':                map_range(float(data['temp_c_average']), -100, 200),
        'solar_current_average':         map_range(float(data['solar_current_average']), -75, 500),
        'voltage_value':                 map_range(float(data['voltage_value']), 0, 6),
        'voltage_average':               map_range(float(data['voltage_average']), 0, 6),
    }
    data.update(fixed_data)

    # Add human-readable data fields
    data['armed_time_hr'] = data['armed_time'] / MS_TO_HOUR
    data['lp_downlink_period_min'] = data['lp_downlink_period'] / MS_TO_MINUTE
    data['transmit_downlink_period_min'] = data['transmit_downlink_period'] / MS_TO_MINUTE
    data['time_alive_day'] = data['time_alive'] / MS_TO_DAY
    data['acs_on_time_min'] = data['acs_on_time'] / MS_TO_MINUTE
    data['rockblock_on_time_min'] = data['rockblock_on_time'] / MS_TO_MINUTE

    # Make faults human-readable
    human_readable_faults = {}
    for key, value in data.items():
        if '_fault' in key:
            #         Bit 0       Bit 1         Bit 2     Bit 3
            labels = ["Signaled", "Suppressed", "Forced", "Base"]
            result = [labels[i] for i in range(4) if value & (1 << i)]
            human_readable_faults[key + '_decoded'] = ", ".join(result) if result else "None"
    data.update(human_readable_faults)

    # Status fields
    data['current_mission_mode'] = data['mission_mode_log'][0]
    data['current_mission_mode_id'] = MISSION_MODE_MAP.get(data['mission_mode_log'][0])
    data['last_command_processed'] = data['command_log'][0]

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


def read_capture_hex_fragment(data: str) -> dict:
    """
    Reads the hexadecimal string of a capture fragment to determine if the
    fragment is the last fragment, which is indicated by the end-marker 'ffd9'.
    Returns the serial number in decimal form, the fragment number in
    decimal form, and the hex string of fragment data needed to be read
    (minus the opcode, capture serial number and fragment number).

    If the capture fragment is not last, the entirety of the fragment portion in hex string
    must be read. If the capture fragment is the last, the hexadecimal string is read up to 'ffd9'.

    Notes:
          - The hex string is the data report minus the op code at the beginning
            (so everything after the op code from the downlink).
          - The serial number is stored in the indices of [0, 2) of the hex string.
          - The fragment number is stored in the indices [8, 10) of the hex string.
            Fragment count starts at 0.
          - The fragment data starts at index 10 and goes to the end of the hex string
            or to the end of end-marker 'ffd9'.
          - The entire hex string for capture fragment data is 80 bytes long.

    :param data: hex string containing capture fragment data
    :return: a dictionary with the fragment's serial #, id #, data, and if the fragment has the end marker
    """

    fragment_number = int(data[8:10], 16)
    end_marker_present = data.count('ffd9') != 0
    fragment_data = data[10:] if not end_marker_present else data[10:data.index('ffd9')+4]
    return {
        'serial_number': int(data[0:2], 16),
        'fragment_number': fragment_number,
        'fragment_data': fragment_data,
        'end_marker_present': end_marker_present
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
    opcode_val = parser.read_uint8()
    if opcode_val in list(map(int, Opcodes)):
        opcode = Opcodes(opcode_val)
    else:
        return error_data('Invalid opcode: ' + str(opcode_val) + '\n')

    # Extract data from report (strip away opcode [0:2])
    data = rockblock_report['data'][2:]

    # Reads data from a packet based on its opcode
    if opcode == Opcodes.normal_report:
        result = compute_normal_report_values(
            parser.read_structure(normal_report_structure))
        # print(result)
    elif opcode == Opcodes.imu_report:
        result = read_imu_hex_fragment(data)
    elif opcode == Opcodes.ods_report:
        result = read_capture_hex_fragment(data)
    result['telemetry_report_type'] = opcode
    return result
