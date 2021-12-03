from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from app.db import db


class EvacuationRouteCoordinate(db.Model):
    __tablename__ = "evacuation_route_coordinates"
    id = Column(Integer, primary_key=True)
    latitude = Column(String(50))
    longitude = Column(String(50))
    evacuation_route_id = Column(Integer, ForeignKey("evacuation_route.id"))
    point = relationship("EvacuationRoute", back_populates="coordinates")
