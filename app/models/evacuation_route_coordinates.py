from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from app.db import db


class EvacuationRouteCoordenate(db.Model):
    __tablename__ = "evacuation_route_coordenates"
    id = Column(Integer, primary_key=True)
    latitude = Column(Integer)
    longitude = Column(Integer)
    evacuation_route_id = Column(Integer, ForeignKey("evacuation_route.id"))
    coordenates = relationship("EvacuationRoute", back_populates="evacuation_route")


# ● Nombre*: nombre de recorrido de evacuación (text).
# ● Descripción de recorrido: información adicional sobre el recorrido (text).
# ● Coordenadas
# 2
# : coordenadas geográficas de los diferentes puntos del recorrido (text).
# Deberán ingresar al menos tres puntos que representen el recorrido de evacuación.
# ● Estado: publicado o despublicado.
