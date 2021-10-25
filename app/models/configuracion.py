from sqlalchemy import Column, Integer, String
from app.db import db

class Configuracion(db.Model):
    __tablename__= "configuracion"
    id = Column(Integer, primary_key=True)
    name = Column(String (30), unique=True)

    def __init__(self, name=None):
        self.name = name