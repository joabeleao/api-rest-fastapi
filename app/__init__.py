'''
Filename: instance.py
Version: 1.0
Author: joabe leão - joabe.leao1@gmail.com

Description:
    App creation, description and instance
'''
from fastapi import FastAPI

from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy import String

from .models.db import Base

app = FastAPI()
#app.config.from_object('config')
# cors
#CORS(app)
#cors = CORS(app, resource={
#    r"/*":{
#        "origins":"*"
#    }
#})



#from .models import users 
#from .routes import routes 
