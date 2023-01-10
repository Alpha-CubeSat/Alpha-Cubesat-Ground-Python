from apifairy import body, other_responses
from flask import Blueprint

from api.schemas import RockblockReportSchema

# from telemetry.telemetry_handler import handle_report
# from telemetry.rockblock_telemetry import verify_rockblock_request, fix_rockbock_datetime

rockblock = Blueprint('rockblock', __name__)

@rockblock.post('/telemetry')
@body(RockblockReportSchema)
@other_responses({401: 'Invalid JWT token'})
def rockblock_telemetry(request):
    """
    Rockblock Telemetry
    Receive data from rockblock web services
    """
    return 'Telemetry not configured yet.', 503

    # try:
    #     verify_rockblock_request(request['JWT'])
    # except:
    #     return '', 401
    # request['transmit_time'] = fix_rockbock_datetime(request['transmit_time'])
    # handle_report(request)
    # return '', 204