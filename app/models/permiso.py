from sqlalchemy import Column, Integer, String
from app.db import db

class Permiso(db.model):
    __tablename__= "permisos"
    id = Column(Integer, primary_key=True)
    name = Column(String (30), unique=True)

    def __init__(self, name=None):
        self.name = name