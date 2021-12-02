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
    coordinates = relationship("EvacuationRouteCoordinate", back_populates="point")
