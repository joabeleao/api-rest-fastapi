'''
Authentication methods
'''
import datetime
import jwt

from werkzeug.security import check_password_hash

from fastapi import Request
from fastapi import HTTPException
from fastapi.security import HTTPBearer
from fastapi.security import HTTPAuthorizationCredentials

from app.views.users import query_user
from app.models.db import SECRET_KEY

class JWTBearer(HTTPBearer):
    '''
    Doc
    '''
    def __init__(self, auto_error: bool = True):
        super(JWTBearer, self).__init__(auto_error=auto_error)

    async def __call__(self, request: Request):
        credentials: HTTPAuthorizationCredentials = await super(JWTBearer, self).__call__(request)
        if credentials:
            if not credentials.scheme == "Bearer":
                raise HTTPException(status_code=403, detail="Invalid authentication scheme.")
            if  self.verify_token(credentials.credentials):
                raise HTTPException(status_code=403, detail="Invalid token or expired token.")
            return credentials.credentials
        raise HTTPException(status_code=403, detail="Invalid authorization code.")

    def verify_token(self, credentials):
        '''
        decorated:
            wraps functions receiving all arguments to
            transform token_decorated function in a proper decorator.
        '''
        print(credentials)
        try:
            token = credentials
            data = jwt.decode(token, SECRET_KEY, algorithms=['HS256'])
            print("here goes data :"+data)
        except Exception:
            return {'message': 'token is invalid or missing', 'data': {} }, 401
    
        print("here goes data :"+data)
        return {"username": "not yet", "token": data}
        #return {"username": current_user.username, "token": "ok"}

def auth(username, password, db_session):
    '''
    auth:
        Get basic auth information and encode it in a token with jwt
    Requires:
        A basic authorization header (username:password base64)
    Returns:
        A valid token
    '''
    user = query_user(username, db_session)

    if user and check_password_hash(user.password, password):
        token = jwt.encode({'username': user.username,
            'exp': datetime.datetime.now() + datetime.timedelta(hours=12) }, SECRET_KEY
        )
        return {'message': 'Validated successfully',
            'token': token,
            'exp': datetime.datetime.now() + datetime.timedelta(hours=12)
        }

    return {'message': 'Invalid username or password', 'data': {} }, 403
