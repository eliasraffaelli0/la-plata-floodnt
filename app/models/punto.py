from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.sql import func
from app.db import db

class Punto(db.Model):
    __tablename__= "puntos_de_encuentro"
    id = Column(Integer, primary_key=True)
    name = Column(String (50), unique=True)
    direccion = Column(String (50))
    coordenadas = Column(String (50), unique=True)
    estado = Column(Integer)
    telefono = Column(String (50))
    email = Column(String (50))
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    created_at = Column(DateTime(timezone=True), server_default=func.now())


    def __init__(self, name=None, direccion=None, coordenadas=None, estado=None, telefono=None, email=None):
        self.name = name
        self.direccion = direccion
        self.coordenadas = coordenadas
        self.estado = estado
        self.telefono = telefono
        self.email = email