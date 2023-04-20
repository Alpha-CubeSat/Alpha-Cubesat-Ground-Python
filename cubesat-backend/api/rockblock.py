import jwt
from apifairy import body, other_responses
from flask import Blueprint

import config
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

    # Verifies the JWT token sent in a rockblock report
    # If JWT is invalid, handle exception and return 401/Unauthorized
    try:
        jwt.decode(report['JWT'], config.rockblock_web_pk, algorithms=['rs256'])
    except:
        return '', 401

    # Fixes the date format of the transmit_time field in the rockblock report.
    # Rockblock uses YY-MM-DD HH:mm:ss as the date format, despite their documentation claiming to
    # use a more standard format: YYYY-MM-DDThh:mm:ssZ. Conversion is done by appending "20" to
    # the start of the date string, which means this fix may not work after the year 2100.

    # print('raw dt:', report['transmit_time'])
    report['transmit_time'] = f"20{report['transmit_time'].replace(' ', 'T')}Z"
    # print('fixed dt:', report['transmit_time'])

    # Decode/process rockblock report and save it in elasticsearch
    telemetry.handle_report(report)  # wrap with try/catch in case of error?

    return '', 204