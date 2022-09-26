from datetime import datetime
from sqlalchemy import create_engine
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import sessionmaker
from app.config import DATABASE_URL
from sqlalchemy.ext.declarative import declarative_base


Base = declarative_base()


def connection_db():
    engine = create_engine(DATABASE_URL, echo=False)
    session = sessionmaker(bind=engine.connect())
    s = session()
    return s


class User(Base):
    __tablename__ = 'Users'

    user_id = Column(Integer, primary_key=True)
    email = Column(String)
    password = Column(String)
    nickname = Column(String)
    created_date = Column(String, default=datetime.now())


class AuthToken(Base):
    __tablename__ = 'AuthToken'

    id = Column(Integer, primary_key=True)
    token = Column(String)
    user_id = Column(Integer)
    created_date = Column(String, default=datetime.now())

