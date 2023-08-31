from apifairy import authenticate, response, other_responses, body, arguments
from flask import Blueprint
from werkzeug.security import generate_password_hash

from api.auth import token_auth
from api.schemas import CreateUserSchema, UsernameSchema, UserSchema, UserListSchema
from api.users_db import get_db

user = Blueprint('user', __name__)

def user_exists(username):
    return get_db().execute('SELECT COUNT(*) FROM user WHERE username = ?', (username,)) \
        .fetchone()[0] != 0

@user.get('/')
@authenticate(token_auth)
@response(UserSchema)
@other_responses({401: 'Invalid access token'})
def get_user():
    """
    Get user info
    Get basic information about the currently logged-in user
    """
    user = token_auth.current_user()
    return {
        **user,
        "is_admin": user['id'] == 1
    }

@user.post('/')
@body(CreateUserSchema)
@authenticate(token_auth)
@response(UsernameSchema)
@other_responses({400: 'User already exists'})
def create_user(req):
    """
    Create user (admin-only)
    """
    if token_auth.current_user()['id'] != 1:
        return 'Forbidden', 403
    if user_exists(req['username']):
        return 'User already exists', 400

    password_hash = generate_password_hash(req['password'])
    get_db().execute('INSERT INTO user (username, password_hash) VALUES (?, ?)',
               (req['username'], password_hash))
    get_db().commit()
    return {'username': req['username']}

@user.delete('/')
@arguments(UsernameSchema)
@authenticate(token_auth)
@other_responses({400: 'User does not exist'})
def delete_user(req):
    """
    Delete user (admin-only)
    """
    if token_auth.current_user()['id'] != 1:
        return 'Forbidden', 403
    if not user_exists(req['username']):
        return 'User does not exist', 400
    if req['username'] == 'admin':
        return 'Not allowed', 400

    get_db().execute('DELETE FROM user WHERE username = ?', (req['username'],))
    get_db().commit()
    return '', 204

@user.get('/list')
@authenticate(token_auth)
@response(UserListSchema)
def list_users():
    """
    Get all users (admin-only)
    """
    if token_auth.current_user()['id'] != 1:
        return 'Forbidden', 403
    query = get_db().execute('SELECT username FROM user').fetchall()
    return {'users': map(lambda x: x[0], query)}
