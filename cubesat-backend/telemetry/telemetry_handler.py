import config
import databases.elastic as es
import telemetry.cubesat_telemetry as cs


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
    es.index(config.rockblock_db_index, es.daily_index_strategy, rockblock_report)

    if rockblock_report['data']:
        result = cs.read_cubesat_data(rockblock_report)
        print('result', result)

        operation = result['telemetry_report_type']
        if operation == cs.Opcodes.normal_report:
            cs.save_cubesat_data(result)
        elif operation == cs.Opcodes.imu_report:
            cs.process_save_deploy_data(result)
        elif operation == cs.Opcodes.camera_report:
            cs.process_save_camera_data(result)
        else: # error_report
            print('Error Report')
    else:
        print('Rockblock report has no "data" attribute')