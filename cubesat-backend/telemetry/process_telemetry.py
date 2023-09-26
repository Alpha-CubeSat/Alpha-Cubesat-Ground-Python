import traceback
from datetime import datetime, timedelta

from config import *
from databases import elastic, image_database
from telemetry.read_telemetry import read_cubesat_data, error_data
from telemetry.telemetry_constants import *

# list of all imu fragment numbers received
fragment_list = []
# keeps track of various stats regarding the received imu fragments
imu_display_info = {'latest_fragment': 0,
                    'missing_fragments': [],
                    'highest_fragment': 0}
first_fragment_time = None

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


def separate_cycles(fragment_number: int, fragment_data: str):
    """
    Decodes imu cycles to retrieve the x, y, and z gyro values for each and saves them to elasticsearch \n
    :param fragment_number: id number of fragment
    :param fragment_data: hex string containing the packet's imu cycle data
    """
    # 462 bytes of imu data sent over 7 packets, end flag (fe92) is present for the last packet
    # each report has 66 bytes of imu data (all 22 cycles are complete) => 154 total cycles
    # 154 cycles * 3 bytes each = 462 bytes
    for x in range(0, len(fragment_data), 6):

        x_gyro = int(fragment_data[x:x + 2], 16)
        y_gyro = int(fragment_data[x + 2:x + 4], 16)
        z_gyro = int(fragment_data[x + 4:x + 6], 16)
        # every full fragment has 22 cycles, new cycle occurs every six digits in the hex string
        cycle_count = fragment_number * CYCLES_PER_FRAGMENT + x / 6

        # Maps imu cycle values from the range used for transmission (0 - 255) to their actual range (-5 - 5)
        # timestamp: 154 total cycles * 250ms per cycle = 38,500 ms => 38.5 seconds
        report_data = {
            'timestamp': first_fragment_time + timedelta(milliseconds=cycle_count * MS_PER_CYCLE),
            'cycle_count': int(cycle_count),
            'x_gyro': float(x_gyro) / 25 - 5,
            'y_gyro': float(y_gyro) / 25 - 5,
            'z_gyro': float(z_gyro) / 25 - 5,
        }
        print('report', report_data)

        # Saves a cycle report to elasticsearch
        elastic.index(cycle_db_index, report_data)


def process_save_deploy_data(data: dict):
    """
    Generates missing imu fragments, processes imu cycles, and saves imu fragment
    summary report (latest, missing, and highest received fragments) to elasticsearch \n
    :param data: dictionary with imu fragment data
    """
    fragment_list.append(data['fragment_number'])
    imu_display_info['latest_fragment'] = data['fragment_number']
    generate_missing_fragments(fragment_list)
    print(fragment_list, imu_display_info)

    # if this is the first IMU fragment, store the time received as the basis
    # for calculating future IMU datapoint timestamps
    global first_fragment_time
    if not first_fragment_time:
        first_fragment_time = datetime.strptime(data['transmit_time'], "%Y-%m-%dT%H:%M:%SZ")
        # offset first fragment time if first fragment is not received first
        if data['fragment_number'] != 0:
            first_fragment_time -= timedelta(milliseconds=data['fragment_number'] * CYCLES_PER_FRAGMENT * MS_PER_CYCLE)

    separate_cycles(data['fragment_number'], data['fragment_data'])
    elastic.index(deploy_db_index, {**report_metadata(data), **imu_display_info})


def process_save_camera_data(data: dict):
    """
    Process image fragment data sent by cubesat. Image comes over several fragments as
    rockblock only supports so much protocol. Image 'fragments' are then assembled into full images
    when fully collected, and saved into the image database. Saves image fragment
    summary report (latest, missing, and highest received fragments) to elasticsearch \n

    :param data: image fragment report
    """
    image_database.save_fragment(data['serial_number'], data['fragment_number'], data['fragment_data'])
    image_database.try_save_image(data['serial_number'], data['max_fragments'])
    elastic.index(image_db_index, {**report_metadata(data), **image_database.get_img_display_info()})

def handle_report(rockblock_report: dict):
    """
    Handles a report sent by the Rockblock web service API as per the Alpha specification.
    Reads the report's opcode and routes it to corresponding data handlers for
    decoding, processing, and storing.

    :param rockblock_report: raw data report from rockblock API
    """

    # Save rockblock report to elasticsearch. Combines latitude and longitude into a single field.
    rockblock_report['location'] = {
        'lat': rockblock_report['iridium_latitude'],
        'lon': rockblock_report['iridium_longitude']
    }

    # if report is not empty, parse and save report
    if rockblock_report['data']:
        try:
            decoded_report = read_cubesat_data(rockblock_report)
            result = {
                **report_metadata(rockblock_report),
                **decoded_report
            }
            print('result', result)
        
            operation = result['telemetry_report_type']
            rockblock_report['telemetry_report_type'] = operation
            if operation == Opcodes.normal_report:
                elastic.index(cubesat_db_index, result)
            elif operation == Opcodes.imu_report:
                process_save_deploy_data(result)
            elif operation == Opcodes.camera_report:
                process_save_camera_data(result)
            else: # Opcodes.error_report
                # either empty data attribute or unknown opcode
                rockblock_report.update(decoded_report)
        except Exception as e:
            print(e)
            # update report to indicate error occurred during processing
            rockblock_report.update(error_data(traceback.format_exc()))
    else:
        rockblock_report.update(error_data('Rockblock report has not "data" attribute'))

    # store rockblock report along with opcode and error message (if error occurred)
    elastic.index(rockblock_db_index, rockblock_report)
