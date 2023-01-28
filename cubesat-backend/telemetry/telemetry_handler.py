import telemetry.cubesat_telemetry as cs
import telemetry.rockblock_telemetry as rb

def handle_cubesat_data(rockblock_report: dict):
    """
    Handles a packet from the cubesat as per the Alpha specification. Reads an opcode,
    and depending on the result, parses and stores the corresponding data

    :param rockblock_report: raw data report from rockblock API
    """

    result = cs.read_cubesat_data(rockblock_report)
    print('result', result)

    operation = result['telemetry_report_type']
    if operation == cs.Opcodes.normal_report:
        cs.save_cubesat_data(result)
    elif operation == cs.Opcodes.deployment_report:
        cs.process_deploy_data(result)
    else: # operation == cs.Opcodes.ttl:
        cs.process_ttl_data(result)

def handle_report(rockblock_report: dict):
    """
    Handles a report sent by the rockblock web service API, decodes from it the cubesat data,
    and routes it to cubesat data handlers.

    :param rockblock_report: raw data report from rockblock API
    """

    rb.save_rockblock_report(rockblock_report)
    if rockblock_report['data']:
        handle_cubesat_data(rockblock_report)
    else:
        print('rockblock report has no "data" attribute')