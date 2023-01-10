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
    elif operation == cs.Opcodes.ttl:
        cs.process_ttl_data(result)
    else:
        raise RuntimeError("Invalid opcode")

def handle_report(rockblock_report: dict):
    """
    Handles a report sent by the rockblock web service API, decodes from it the cubesat data,
    and routes it to cubesat data handlers.

    :param rockblock_report: raw data report from rockblock API
    """

    rb.save_rockblock_report(rockblock_report)
    if rockblock_report['data']:
        handle_cubesat_data(rockblock_report)
    # (http/ok)

"""
# http web server related stuff ---------------------------------------------------------

# Middleware that verifies the JWT sent in a rockblock report, and extracts the data.
# Does not use data sent in report, but instead that which is decoded from the provided JWT since it is an exact copy.
def verify_rockblock_data_mw(request):
    try:
        rb.verify_rockblock_request(request['JWT'])
    except:
        pass
        # (http/unauthorized)

# Middleware that fixes the date format in data from rockblock web services.
def fix_rockblock_date_mw(request):
    request['transmit_time'] = rb.fix_rockbock_datetime(request['transmit_time'])
"""