from datetime import datetime
from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base


Base = declarative_base()


class User(Base):
    __tablename__ = 'Users'

    user_id = Column(Integer, primary_key=True)
    email = Column(String)
    password = Column(String)
    nickname = Column(String)
    created_date = Column(String, default=str(datetime.now()))


class AuthToken(Base):
    __tablename__ = 'AuthToken'

    id = Column(Integer, primary_key=True)
    token = Column(String)
    user_id = Column(Integer)
    created_date = Column(String, default=str(datetime.now()))

