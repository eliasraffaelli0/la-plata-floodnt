from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.models.permiso import Permiso
from app.db import db


class Punto(db.Model):
    __tablename__ = "puntos_de_encuentro"
    id = Column(Integer, primary_key=True)
    name = Column(String(50), unique=True)
    address = Column(String(50))
    latitude = Column(String(50), unique=True)
    longitude = Column(String(50), unique=True)
    state = Column(Integer)
    telephone = Column(String(50))
    email = Column(String(50))
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    created_at = Column(DateTime(timezone=True), server_default=func.now())
