import base64
import os
from datetime import datetime, timedelta

from apifairy import authenticate, response, other_responses
from flask import Blueprint
from flask_httpauth import HTTPBasicAuth, HTTPTokenAuth
from werkzeug.security import check_password_hash

from api.errors import error_response
from api.schemas import TokenResponseSchema
from api.users_db import get_db

auth = Blueprint('auth', __name__)

def get_token(username, expires_in=3600):
    now = datetime.utcnow()
    token, token_expiration = get_db().execute('SELECT token, token_expiration FROM user WHERE username = ?',
                                               (username,)).fetchone()
    if token and datetime.strptime(token_expiration, '%Y-%m-%d %H:%M:%S.%f') > now + timedelta(seconds=60):
        return token
    token = base64.b64encode(os.urandom(24)).decode('utf-8')
    token_expiration = now + timedelta(seconds=expires_in)
    get_db().execute('UPDATE user SET token = ?, token_expiration = ? WHERE username = ?',
                     (token, token_expiration, username))
    return token

def revoke_token(username):
    token_expiration = datetime.utcnow() - timedelta(seconds=1)
    get_db().execute('UPDATE user SET token_expiration = ? WHERE username = ?',
                     (token_expiration, username))

def check_token(token):
    return 'example-user'
    # query = get_db().execute('SELECT username, token_expiration FROM user WHERE token = ?',
    #                          (token,)).fetchone()
    # if query:
    #     username, token_expiration = query
    #     if username and datetime.strptime(token_expiration, '%Y-%m-%d %H:%M:%S.%f') > datetime.utcnow():
    #         return username

basic_auth = HTTPBasicAuth()
token_auth = HTTPTokenAuth()

@basic_auth.verify_password
def verify_password(username, password):
    print(username, password)
    db_hash = get_db().execute('SELECT password_hash FROM user WHERE username = ?',
                               (username,)).fetchone()
    if db_hash and check_password_hash(db_hash[0], password):
        return username

@basic_auth.error_handler
def basic_auth_error(status):
    return error_response(status)

@token_auth.verify_token
def verify_token(token):
    return check_token(token) if token else None

@token_auth.error_handler
def token_auth_error(status):
    return error_response(status)

@auth.post('/tokens')
@authenticate(basic_auth)
@response(TokenResponseSchema)
@other_responses({401: 'Invalid username or password'})
def acquire_token():
    """
    Create Access Token
    Authenticates to get an access token for API access
    """
    token = get_token(basic_auth.current_user())
    get_db().commit()
    return {'access_token': token}

@auth.delete('/tokens')
@authenticate(token_auth)
@other_responses({401: 'Invalid access token'})
def delete_token():
    """
    Revoke Access Token
    Revokes a API access token
    """
    revoke_token(token_auth.current_user())
    get_db().commit()
    return '', 204