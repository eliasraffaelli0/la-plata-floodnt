from sqlalchemy import Column, Integer, String
from app.db import db


class Configuracion(db.Model):
    __tablename__ = "configuracion"
    id = Column(Integer, primary_key=True)
    elementos_por_pagina = Column(Integer)
    tema_publico = Column(String(20))
    tema_privado = Column(String(20))
    criterio_de_ordenacion = Column(String(50))
