from sqlalchemy import Column, String, Integer, Date
from sqlalchemy.orm import declarative_base
import datetime as dt

Base = declarative_base()

class login(Base):
    __tablename__ = 'login'

    id = Column(Integer, primary_key=True)
    username = Column(String)
    password = Column(String)
    email = Column(String)
    created_at = Column(Date, default=dt.datetime.now())
    updated_at = Column(Date, default=dt.datetime.now())

    def __init__(self, username, password, email):
        self.username = username
        self.password = password
        self.email = email

    def __repr__(self):
        return f"({self.username}, {self.password}, {self.email})"

class chat(Base):
    __tablename__ = 'chat'

    id = Column(Integer, primary_key=True)
    username = Column(String)
    message = Column(String)
    created_at = Column(Date, default=dt.datetime.now())

    def __init__(self, username, message):
        self.username = username
        self.message = message

    def __repr__(self):
        return f"({self.username}, {self.message})"