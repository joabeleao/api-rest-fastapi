'''
Filename: run.py
Version: 1.0
Author: joabe leão - joabe.leao1@gmail.com

Description:
    App creation, documentation and instance
'''
from fastapi import Depends
from fastapi import Request
#from fastapi import Body

from sqlalchemy.orm import Session

from app import app
from app.models import users
from app.models.db import engine
from app.models.db import SessionLocal
from app.views.users import post_user
from app.views.users import update_user
from app.views.users import delete_user
from app.views.users import get_users
from app.views.users import get_user
from app.views import helper

from fastapi.security import HTTPBasic, HTTPBasicCredentials

#create the database tables on app startup or reload
users.Base.metadata.create_all(bind=engine)

def get_db():
    '''
    Doc
    '''
    db_session = SessionLocal()
    try:
        yield db_session
    finally:
        db_session.close()


security = HTTPBasic()
nsession:Session = Depends(get_db)

@app.post("/auth")
def authenticate(credentials: HTTPBasicCredentials = Depends(security), \
        db_session:Session = Depends(get_db)):
    '''
    Doc
    '''
    if not credentials:
        return {'message': 'Unauthorized',
            'WWW-Authenticate': 'Basic auth=login and password required'
        }, 401

    token = helper.auth(username=credentials.username, password=credentials.password, \
            db_session=db_session)

    return {"message": credentials.username, "token": token, "credentials": credentials.password}

@app.get("/")
def root():
    '''
    Doc
    '''
    return {"message": "Hello World"}

@app.get("/users", dependencies=[Depends(helper.JWTBearer())])
async def users_get(db_session:Session = Depends(get_db)):
    '''
    Doc
    '''
    return get_users(db_session=db_session)

@app.get("/user/{user_id}")
async def userid_get(user_id:str, db_session:Session = Depends(get_db)):
    '''
    Doc
    '''
    return get_user(db_session=db_session, user_id=user_id)

@app.post("/user")
async def user_post(request: Request, db_session:Session = Depends(get_db)):
    '''
    Doc
    '''
    request = await request.json()

    new_user = post_user(db_session=db_session, username=request['username'], \
            password=request['password'], name=request['name'], email=request['email'])

    return new_user

@app.put("/user/{user_id}")
async def user_put(request: Request, user_id:str, db_session:Session = Depends(get_db)):
    '''
    Doc
    '''
    request = await request.json()

    updated_user = update_user(db_session=db_session, user_id=user_id, \
            username=request['username'], password=request['password'], \
                    name=request['name'], email=request['email'])

    return updated_user

@app.delete("/user/{user_id}")
async def userid_delete(user_id:str, db_session:Session = Depends(get_db)):
    '''
    Doc
    '''
    return delete_user(db_session=db_session, user_id=user_id)

#@app.post("/user")
#def user_post(request: dict = Body(), db_session:Session = Depends(get_db)):
#    '''
#    Doc
#    '''
#    print(request['name'])
#    newuser = post_user(db_session=db_session, username=request['username'], \
#            password=request['password'], name=request['name'], email=request['email'])
#
#    return {"user": newuser}

#@app.post("/user")
#def user_post(username:str, password:str, name:str, email:str, \
#        db_session:Session = Depends(get_db)):
#    '''
#    Doc
#    '''
#    friend = post_user(db_session=db_session, username=username, \
#            password=password, name=name, email=email)
###return object created
#    return {"friend": friend}
