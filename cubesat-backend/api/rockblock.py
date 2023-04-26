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
    print("report received")
    # print(report)

    # Verifies the JWT token sent in a rockblock report
    # If JWT is invalid, handle exception and return 401/Unauthorized
    try:
        jwt.decode(report['JWT'], config.rockblock_web_pk, algorithms=['RS256'])
    except:
        print('JWT verification error')
        return '', 401

    # Fixes the date format of the transmit_time field in the rockblock report.
    # Rockblock uses YY-MM-DD HH:mm:ss as the date format instead of the YYYY-MM-DDThh:mm:ssZ
    # standard format. Conversion is done by appending "20" to the start of the date string,
    # which means this fix may not work after the year 2100.
    report['transmit_time'] = f"20{report['transmit_time'].replace(' ', 'T')}Z"

    # Decode/process rockblock report and save it in elasticsearch
    telemetry.handle_report(report)  # wrap with try/catch in case of error?
    print("report processed")

    return '', 200 # Successful downlink code