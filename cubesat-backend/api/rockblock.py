from apifairy import body, other_responses
from flask import Blueprint

import telemetry.rockblock_telemetry as rb
import telemetry.telemetry_handler as telemetry
from api.schemas import RockblockReportSchema

rockblock = Blueprint('rockblock', __name__)

@rockblock.post('/telemetry')
@body(RockblockReportSchema)
@other_responses({401: 'Invalid JWT token'})
def rockblock_telemetry(report):
    """
    Rockblock Telemetry
    Receive data from rockblock web services
    """

    # Verifies the JWT sent in a rockblock report
    # If JWT is invalid, handle exception and return 401/Unauthorized
    try:
        rb.verify_rockblock_request(report['JWT'])
    except:
        return '', 401

    # Fixes the date format in data from rockblock web services.
    report['transmit_time'] = rb.fix_rockbock_datetime(report['transmit_time'])

    # Decode/process rockblock report and save it in elasticsearch
    telemetry.handle_report(report)  # wrap with try/catch in case of error?

    return '', 204