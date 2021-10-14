from sqlalchemy import Column, Integer, String
from app.db import db

class User(db.Model):
    __tablename__= "ususarios"
    id = Column(Integer, primary_key=True)
    email = Column(String (30), unique=True)
    username = Column(String (30), unique=True)
    password = Column(String (30), unique=True)
    first_name = Column(String (30), unique=True)
    last_name = Column(String (30), unique=True)


def __init__(self, email=None, username=None, password=None, first_name=None, last_name=None):
    self.email = email
    self.username = username
    self.password = password
    self.first_name = first_name
    self.last_name = last_name