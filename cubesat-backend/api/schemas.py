from marshmallow import INCLUDE

from api.app import ma


class RockblockReportSchema(ma.Schema):
    class Meta:
        unknown = INCLUDE

    imei = ma.Int(required=True)
    JWT = ma.Str(required=True)
    transmit_time = ma.Str(required=True)
    iridium_longitude = ma.Float(required=True)
    iridium_latitude = ma.Float(required=True)
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

class CommandUplinkSchema(ma.Schema):
    imei = ma.Str(required=True)
    commands = ma.Nested(CommandSchema(many=True), required=True)

class CommandResponseSchema(ma.Schema):
    status = ma.Str(required=True)
    timestamp = ma.Str(required=True)
    imei = ma.Str(required=True)
    commands = ma.Nested(CommandSchema(many=True), required=True)
    message = ma.Str(required=True)

class TokenResponseSchema(ma.Schema):
    access_token = ma.Str(required=True)

class UsernameSchema(ma.Schema):
    username = ma.Str(required=True)

class CreateUserSchema(ma.Schema):
    username = ma.Str(required=True)
    password = ma.Str(required=True)

class UserSchema(ma.Schema):
    id = ma.Int(required=True)
    username = ma.Str(required=True)
    is_admin = ma.Bool()

class UserListSchema(ma.Schema):
    users = ma.List(ma.Str())