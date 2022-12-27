from flask import Blueprint, make_response

auth = Blueprint('auth', __name__)

@auth.post('/login')
def login():
    return make_response('Login not configured yet.', 503)