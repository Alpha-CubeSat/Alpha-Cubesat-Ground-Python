from apifairy import body, response
from flask import Blueprint

from api.schemas import SimpleStringSchema

debug = Blueprint('debug', __name__)

@debug.get('/ping')
@response(SimpleStringSchema)
def ping():
    """
    Ping
    Send a ping request to the API
    """
    return {'response': 'pong'}

@debug.post('/echo')
@body(SimpleStringSchema)
@response(SimpleStringSchema)
def echo(request):
    """
    Echo
    Echos a request for debugging purposes
    """
    return request