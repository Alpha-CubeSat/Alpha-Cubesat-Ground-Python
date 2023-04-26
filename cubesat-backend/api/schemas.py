from api.app import ma

class RockblockReportSchema(ma.Schema):
    device_type = ma.Str()
    imei = ma.Int()
    serial = ma.Int()
    momsn = ma.Int()
    JWT = ma.Str()
    transmit_time = ma.Str()
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
    opcode = ma.Str(required=True)
    namespace = ma.Str()
    field = ma.Str()
    value = ma.Raw()

class CommandResponseSchema(ma.Schema):
    status = ma.Str(required=True)
    timestamp = ma.Str(required=True)
    commands = ma.Nested(CommandSchema(many=True), required=True)
    message = ma.Str()

class TokenResponseSchema(ma.Schema):
    access_token = ma.Str(required=True)