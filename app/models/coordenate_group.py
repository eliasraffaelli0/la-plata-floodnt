from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.db import db


class Point_Group(db.Model):
    __tablename__ = "point_group"
    id = Column(Integer, primary_key=True)
    name = Column(String(50), unique=True)
    state = Column(String(50))
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    type = Column(String(50))
    __mapper_args__ = {"polymorphic_identity": "point_group", "polymorphic_on": type}


# nombre
# estado
# coordenadas(relacion)
# recorrido
# ● Descripción de recorrido: información adicional sobre el recorrido (text).
# ● Coordenadas2: coordenadas geográficas de los diferentes puntos del recorrido (text).
# Deberán ingresar al menos tres puntos que representen el recorrido de evacuación.

# zona
# Código de zona: identificador unívoco de la zona inundable
# ● Coordenadas1: coordenadas geográficas (al menos tres puntos) de la zona
# inundable (text)
# ● Color capa
