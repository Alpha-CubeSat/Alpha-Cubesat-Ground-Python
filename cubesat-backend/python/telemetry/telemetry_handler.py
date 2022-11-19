import telemetry.cubesat_telemetry as cs
import telemetry.rockblock_telemetry as rb
# :require [ring.util.http-response :as http]

# Handles a packet from the cubesat as per the Alpha specification. Reads an opcode,
# and depending on the result, parses and stores the corresponding data
def handle_cubesat_data(rockblock_report):
  result = cs.read_cubesat_data(rockblock_report)
  operation = result['telemetry-report-type']
  if operation == cs.opcodes.normal_report:
    cs.save_cubesat_data(result)
  elif operation == cs.opcodes.deployment_report:
    cs.process_deploy_data(result)
  elif operation == cs.opcodes.ttl:
    cs.process_ttl_data(result)

# Handles a report sent by the rockblock web service API, decodes from it the cubesat data,
# and routes it to cubesat data handlers.
def handle_report(rockblock_report):
  rb.save_rockblock_report(rockblock_report)
  if rockblock_report['data']:
    handle_cubesat_data(rockblock_report)
  # (http/ok)

# Middleware that verifies the JWT sent in a rockblock report, and extracts the data.
# Does not use data sent in report, but instead that which is decoded from the provided JWT since it is an exact copy.
def verify_rockblock_data_mw(handler):
  def internal(request):
    verified_data = rb.verify_rockblock_request(request['body-params'])
    request['body-params'] = verified_data
    if handler(request):
      pass
      # (http/unauthorized)
  return internal

# Middleware that fixes the date format in data from rockblock web services.
def fix_rockblock_date_mw(handler):
  def internal(request):
    time = request['body-params']['transmit_time']
    formatted_time = rb.fix_rb_datetime(time)
    request['body-params']['transmit_time'] = formatted_time
    handler(request)
  return internal