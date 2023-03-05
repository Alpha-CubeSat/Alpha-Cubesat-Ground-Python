from api.app import ma

class SimpleStringSchema(ma.Schema):
    response = ma.Str(required=True)

class RockblockReportSchema(ma.Schema):
    device_type = ma.Str()
    iss = ma.Str()
    imei = ma.Int()
    serial = ma.Int()
    iat = ma.Int()
    momsn = ma.Int()
    JWT = ma.Str()
    transmit_time = ma.DateTime()
    iridium_session_status = ma.Int()
    iridium_longitude = ma.Float()
    iridium_latitude = ma.Float()
    iridium_cep = ma.Float()
    data = ma.Str(required=True)

class ImageCountSchema(ma.Schema):
    count = ma.Int(load_default=5)

class ImageNameSchema(ma.Schema):
    images = ma.List(ma.Str())

class ImageDataSchema(ma.Schema):
    name = ma.Str(required=True)
    timestamp = ma.Str(required=True)
    base64 = ma.Str(required=True)

class CommandSchema(ma.Schema):
    operation = ma.Str(required=True)
    args = ma.List(ma.Str())

class CommandResponseSchema(ma.Schema):
    status = ma.Str(required=True)
    timestamp = ma.Str(required=True)
    commands = ma.Nested(CommandSchema(many=True), required=True)
    error_code = ma.Str()
    error_message = ma.Str()

class TokenResponseSchema(ma.Schema):
    access_token = ma.Str(required=True)