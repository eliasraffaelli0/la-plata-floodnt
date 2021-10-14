from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.sql import func
from app.db import db

class User(db.Model):
    __tablename__= "usuarios"
    id = Column(Integer, primary_key=True)
    email = Column(String (30), unique=True)
    username = Column(String (30), unique=True)
    password = Column(String (30))
    activo = Column(Integer)
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    first_name = Column(String (30))
    last_name = Column(String (30))


def __init__(self, email=None, username=None, activo=None, password=None, first_name=None, last_name=None):
    self.email = email
    self.username = username
    self.password = password
    self.activo = activo
    self.first_name = first_name
    self.last_name = last_name