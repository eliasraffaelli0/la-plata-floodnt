from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql.sqltypes import Float
from app.db import db


class EvacuationRouteCoordinate(db.Model):
    __tablename__ = "evacuation_route_coordinates"
    id = Column(Integer, primary_key=True)
    latitude = Column(Float)
    longitude = Column(Float)
    evacuation_route_id = Column(Integer, ForeignKey("evacuation_route.id"))
    point = relationship("EvacuationRoute", back_populates="coordinates")


# ● Nombre*: nombre de recorrido de evacuación (text).
# ● Descripción de recorrido: información adicional sobre el recorrido (text).
# ● Coordenadas
# 2
# : coordenadas geográficas de los diferentes puntos del recorrido (text).
# Deberán ingresar al menos tres puntos que representen el recorrido de evacuación.
# ● Estado: publicado o despublicado.
