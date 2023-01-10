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
    count = ma.Int(load_default=1)

class ImageNameSchema(ma.Schema):
    name = ma.Str(required=True)

class ImageDataSchema(ma.Schema):
    name = ma.Str(required=True)
    date = ma.DateTime(required=True)
    base64 = ma.Str(required=True)

class CommandSchema(ma.Schema):
    type = ma.Str(required=True) # enum?
    fields = ma.Dict(keys=ma.Str(), values=ma.Str()) # dict types?

class CommandResponseSchema(ma.Schema):
    status = ma.Str(required=True)
    id = ma.Int()
    error_code = ma.Int()
    description = ma.Str()

class TokenResponseSchema(ma.Schema):
    access_token = ma.Str(required=True)