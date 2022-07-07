'''
Database models creation
'''
from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy import DateTime
from sqlalchemy.sql import func

from app.models.db import Base

class Users(Base):
    '''
        User's table, class and field definition
    '''
    # table
    __tablename__ = "users"

    # fields
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    username = Column(String(20), unique=True, nullable=False)
    password = Column(String(200), nullable=False)
    name = Column(String(80), nullable=False)
    email = Column(String(60), unique=True,nullable=False)
    created_on = Column(DateTime(timezone=True), server_default=func.now())
