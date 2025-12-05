import traceback

from api.webhook import send_webhook_message
from config import *
from databases import elastic, capture_database, command_log
from telemetry.read_telemetry import read_cubesat_data, error_data, map_range
from telemetry.telemetry_constants import *

# list of all imu fragment numbers received
fragment_list = []
# keeps track of various stats regarding the received imu fragments
imu_display_info = {'latest_fragment': 0, 'missing_fragments': [], 'highest_fragment': 0, 'fragment_count': f'0/{TOTAL_IMU_REPORTS}'}


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
    imu_display_info['fragment_count'] = f'{len(frag_list)}/{TOTAL_IMU_REPORTS}'
    for x in range(max_frag):
        if frag_list.count(x) == 0:
            imu_display_info['missing_fragments'].append(x)


def process_save_deploy_data(data: dict):
    """
    Generates missing imu fragments, processes imu cycles, and saves imu fragment
    summary report (latest, missing, and highest received fragments) to elasticsearch \n
    :param data: dictionary with imu fragment data
    """
    fragment_number, fragment_data = data['fragment_number'], data['fragment_data']
    fragment_list.append(fragment_number)
    imu_display_info['latest_fragment'] = fragment_number
    generate_missing_fragments(fragment_list)

    # 1188 bytes of imu data sent over 18 packets, end flag (fe92) is present for the last packet
    # each report has 66 bytes of imu data (all 22 cycles are complete) => 396 total cycles
    # 396 cycles * 3 bytes each = 1188 bytes
    for x in range(0, len(fragment_data), 6):
        x_gyro = int(fragment_data[x:x + 2], 16)
        y_gyro = int(fragment_data[x + 2:x + 4], 16)
        z_gyro = int(fragment_data[x + 4:x + 6], 16)

        # every full fragment has 22 cycles, new cycle occurs every six digits in the hex string
        cycle_count = fragment_number * CYCLES_PER_FRAGMENT + x / 6

        # Maps imu cycle values from the range used for transmission (0 - 255) to their actual range (-10 - 10)
        report_data = {
            **report_metadata(data),
            'cycle_count': int(cycle_count),
            'x_gyro': map_range(float(x_gyro), -10, 10),
            'y_gyro': map_range(float(y_gyro), -10, 10),
            'z_gyro': map_range(float(z_gyro), -10, 10),
        }

        # Saves a cycle report to elasticsearch
        elastic.index(cycle_db_index, report_data)

    # Save IMU report downlink progress to elasticsearch
    elastic.index(deploy_db_index, {**report_metadata(data), **imu_display_info})


def process_save_ods_data(data: dict):
    """
    Process capture fragment data sent by cubesat. Capture comes over several fragments as
    rockblock only supports so much protocol. Capture 'fragments' are then assembled into full captures
    when fully collected, and saved into the capture database. Saves capture fragment
    summary report (latest, missing, and highest received fragments) to elasticsearch \n

    :param data: capture fragment report
    """
    capture_database.save_fragment(data['imei'], data['serial_number'], data['fragment_number'], data['fragment_data'])
    capture_database.try_save_capture(data['imei'], data['serial_number'], data['end_marker_present'])

    # Save camera report downlink progress to elasticsearch
    elastic.index(capture_db_index,
                  {**report_metadata(data), **capture_database.capture_fragment_downlink_info})


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
            print('decoded report:')
            print(result)

            operation = result['telemetry_report_type']
            rockblock_report['telemetry_report_type'] = operation # (needed for downlink history)
            if operation == Opcodes.normal_report:
                command_log.update_command_log(result['imei'], result['command_log'])
                response = elastic.index(cubesat_db_index, result)
                # id of normal report entry in elasticsearch (needed for downlink history)
                if response: rockblock_report['normal_report_id'] = response.body["_id"]
            elif operation == Opcodes.imu_report:
                process_save_deploy_data(result)
            elif operation == Opcodes.ods_report:
                process_save_ods_data(result)
        except Exception as e:
            print(traceback.format_exc())
            # update report to indicate error occurred during processing
            rockblock_report.update(error_data(traceback.format_exc()))
    else:
        rockblock_report.update(error_data('Rockblock report has not "data" attribute\n'))

    # store rockblock report along with opcode and error message (if error occurred)
    response = elastic.index(rockblock_db_index, rockblock_report)

    # Send message to Slack if report is from flight unit
    if rockblock_report['imei'] == 300534060424390:
        try:
            if rockblock_report['telemetry_report_type'] == Opcodes.normal_report:
                report_link = f"{kibana_base}/discover#/doc/7ec3ba94-572b-47cb-b1f1-ff41830a4eed/cubesat_normal_report?id={rockblock_report.get('normal_report_id', '')}"
            else:
                report_link = f"{kibana_base}/discover#/doc/be8ff1eb-1f57-4782-8807-611d9332ef2d/rockblock_data?id={response.body.get('_id', '')}"
            send_webhook_message(
                f"New *CubeSat {str(rockblock_report['telemetry_report_type'])} Report* Received!" +
                f"\n<{kibana_base}/dashboards#/view/a53a753f-8750-4625-b428-fbfdc350ee1f|View Mission Ops Dashboard>"
                f"\n<{report_link}|View Report>"
            )
        except:
            print("error sending webhook")
