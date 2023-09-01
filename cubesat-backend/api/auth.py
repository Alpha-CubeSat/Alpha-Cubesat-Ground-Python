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

basic_auth = HTTPBasicAuth()
token_auth = HTTPTokenAuth()

@basic_auth.verify_password
def verify_password(username, password):
    query = get_db().execute('SELECT id, password_hash FROM user WHERE username = ?',
                               (username,)).fetchone()
    if query:
        id, pw_hash = query
        if check_password_hash(pw_hash, password):
            return {
                'id': id,
                'username': username
            }

@basic_auth.error_handler
def basic_auth_error(status):
    return error_response(status)

@token_auth.verify_token
def verify_token(token):
    query = get_db().execute('SELECT id, username, token_expiration FROM user WHERE token = ?',
                             (token,)).fetchone()
    if query:
        id, username, token_expiration = query
        if username and datetime.strptime(token_expiration, '%Y-%m-%d %H:%M:%S.%f') > datetime.utcnow():
            return {
                'id': id,
                'username': username
            }

@token_auth.error_handler
def token_auth_error(status):
    return error_response(status)

@auth.post('/token')
@authenticate(basic_auth)
@response(TokenResponseSchema)
@other_responses({401: 'Invalid username or password'})
def get_token():
    """
    Create Access Token
    Authenticates to get an access token for API access
    """
    token = base64.b64encode(os.urandom(24)).decode('utf-8')
    token_expiration = datetime.utcnow() + timedelta(weeks=1) # when deployed this should be < 1 day
    get_db().execute('UPDATE user SET token = ?, token_expiration = ? WHERE username = ?',
                     (token, token_expiration, basic_auth.current_user()['username']))
    get_db().commit()
    return {'access_token': token}

@auth.delete('/token')
@authenticate(token_auth)
@other_responses({401: 'Invalid access token'})
def delete_token():
    """
    Revoke Access Token
    Revokes a API access token
    """
    token_expiration = datetime.utcnow() - timedelta(seconds=1)
    get_db().execute('UPDATE user SET token_expiration = ? WHERE username = ?',
                     (token_expiration, token_auth.current_user()['username']))
    get_db().commit()
    return '', 204
