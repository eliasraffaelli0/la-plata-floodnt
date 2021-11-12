from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.db import db


class EvacuationRoute(db.Model):
    __tablename__ = "evacuation_route"
    id = Column(Integer, primary_key=True)
    name = Column(String(50), unique=True)
    description = Column(String(50))
    state = Column(Integer)
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    coordenates = relationship("EvacuationRouteCoordinate", back_populates="point")


# ● Nombre*: nombre de recorrido de evacuación (text).
# ● Descripción de recorrido: información adicional sobre el recorrido (text).
# ● Coordenadas
# 2
# : coordenadas geográficas de los diferentes puntos del recorrido (text).
# Deberán ingresar al menos tres puntos que representen el recorrido de evacuación.
# ● Estado: publicado o despublicado.
