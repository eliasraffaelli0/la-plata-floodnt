from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from app.db import db


class ZoneCoordinate(db.Model):
    tablename = "zone_coordinates"
    id = Column(Integer, primary_key=True)
    latitude = Column(String(100))
    longitude = Column(String(100))
    zone_id = Column(Integer, ForeignKey("zone.id"))
    point = relationship("Zone", back_populates="coordinates")
