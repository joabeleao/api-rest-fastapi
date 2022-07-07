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

@app.get("/")
def root():
    '''
    Doc
    '''
    return {"message": "Hello World"}

@app.post("/user")
async def user_post(request: Request, db_session:Session = Depends(get_db)):
    '''
    Doc
    '''
    request = await request.json()

    newuser = post_user(db_session=db_session, username=request['username'], \
            password=request['password'], name=request['name'], email=request['email'])

    return newuser

@app.put("/user/{id}")
async def user_put(request: Request, user_id, db_session:Session = Depends(get_db)):
    '''
    Doc
    '''
    request = await request.json()

    #updated_user = update_user(db_session=db_session, username=request['username'], \
    #        password=request['password'], name=request['name'], email=request['email'])

    #return updated_user
    return user_id

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
