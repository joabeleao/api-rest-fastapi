'''
Authentication methods
'''
from functools import wraps

import datetime
import jwt

from flask import jsonify
from flask import request
from werkzeug.security import check_password_hash

from app import app
from app.views.users import query_user

def token_required(wraped_func):
    '''
    token_required:
       Decorator function used by endpoints to check if
       a valid token was given in order to access the route.
    Validations:
        verify if token exists
        verify its expiratin date
        decode token with secret defined on config.py
    '''
    @wraps(wraped_func)
    def decorated(*args, **kwargs):
        '''
        decorated:
            wraps functions receiving all arguments to
            transform token_decorated function in a proper decorator.
        '''
        try:
            # token filter - e.g: Authorization: Bearer tokenhash
            token = request.headers.get('Authorization').split(' ')[1]
        except Exception:
            try:
                # token filter - e.g: Authorization: tokenhash
                token = request.headers.get('Authorization')
            except Exception:
                return jsonify({'message': 'token is invalid or missing', 'data': {} }), 401

        if not token:
            return jsonify({'message': 'token is invalid or missing', 'data': {} }), 401
        try:
            data = jwt.decode(token, app.config['SECRET_KEY'], algorithms=['HS256'])
            current_user = query_user(username=data['username'])
        except Exception:
            return jsonify({'message': 'token is invalid or expired', 'data': {} }), 403
        return wraped_func(current_user.username, *args, **kwargs)
    return decorated

def auth():
    '''
    auth:
        Get basic auth information and encode it in a token with jwt
    Requires:
        A basic authorization header (username:password base64)
    Returns:
        A valid token
    '''
    try:
        auth_data = request.authorization
    except Exception:
        return jsonify({'message': 'Unauthorized',
            'WWW-Authenticate': 'Basic auth=login and password required'
        }), 401

    if not auth_data or not auth_data.username or not auth_data.password:
        return jsonify({'message': 'Unauthorized',
            'WWW-Authenticate': 'Basic auth=login and password required'
        }), 401

    user = query_user(auth_data.username)

    if user and check_password_hash(user.password, auth_data.password):
        token = jwt.encode({'username': user.username,
            'exp': datetime.datetime.now() + datetime.timedelta(hours=12) },
            app.config['SECRET_KEY']
        )
        return jsonify({'message': 'Validated successfully',
            'token': token,
            'exp': datetime.datetime.now() + datetime.timedelta(hours=12)
        })

    return jsonify({'message': 'Invalid username or password', 'data': {} }), 403
