from apifairy import body, authenticate
from flask import Blueprint

from api.auth import chipsat_basic_auth
from api.schemas import ChipSatReportSchema

chipsat = Blueprint('chipsat', __name__)


@chipsat.post('/telemetry')
@authenticate(chipsat_basic_auth)
@body(ChipSatReportSchema)
def chipsat_telemetry(packet):
    """
    ChipSat Telemetry
    Used to receive downlinked packets sent by the ChipSat from TinyGS.
    Must have a valid auth.
    """
    # packet = request.get_json(force=True)
    print('packet received:')
    print(packet)

    # payload = packet['parsed']['payload']
    # gyro_bias = chipsat_gyro_bias_map[payload['chipsatId']]
    # data = {
    #     "timestamp": datetime.fromtimestamp(packet['serverTime']/1000, timezone.utc).isoformat(),
    #     "tinygsPacketId": packet['id'],
    #     "data": base64.b64decode(packet['raw']).hex(),
    #     "chipsatId": payload['chipsatId'],
    #     "location": {
    #         "lat": payload['latitudeDeg'],
    #         "lon": payload['longitudeDeg'],
    #     },
    #     "altitude": payload['altitudeM'],
    #     "gyroX": payload['gyroXDps'] + gyro_bias['x'],
    #     "gyroY": payload['gyroYDps'] + gyro_bias['y'],
    #     "gyroZ": payload['gyroZDps'] + gyro_bias['z'],
    #     # We need to map the acceleration values ourselves since the decoder is wrong
    #     "accelX": -10 + (20 / 255.0) * payload['accelXRaw'],
    #     "accelY": -10 + (20 / 255.0) * payload['accelYRaw'],
    #     "accelZ": -10 + (20 / 255.0) * payload['accelZRaw'],
    #     "magX": payload['magXUT'],
    #     "magY": payload['magYUT'],
    #     "magZ": payload['magZUT'],
    #     "temperature": payload['temperatureC'],
    #     "gpsPositionValid": payload['gpsPositionValid'],
    #     "gpsAltitudeValid": payload['gpsAltitudeValid'],
    #     "imuValid": payload['imuValid'],
    #     "gpsOn": payload['gpsOn'],
    #     "listenFlag": payload['lFlag'],
    #     "validUplinks": payload['validUplinks'],
    #     "invalidUplinks": payload['invalidUplinks'],
    # }
    # elastic.index(config.chipsat_db_index, data)
    print('packet processed')

    return '', 200  # Successful downlink code
