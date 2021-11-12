from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.db import db


class Point_group(db.Model):
    __tablename__ = "point_group"
    id = Column(Integer, primary_key=True)
    name = Column(String(50), unique=True)
    state = Column(String(50))
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    type = Column(String(50))
    coordenates = relationship("Coordenate", back_populates="point_group")

    __mapper_args__ = {"polymorphic_identity": "point_group", "polymorphic_on": type}


class Evacuation_route(Point_group):
    __tablename__ = "evacuation_route"
    id = Column(Integer, ForeignKey("point_group.id"), primary_key=True)
    evacuation_route_name = Column(String(50))

    __mapper_args__ = {"polymorphic_identity": "evacuation_route"}


class Zone(Point_group):
    __tablename__ = "zone"
    id = Column(Integer, ForeignKey("point_group.id"), primary_key=True)
    zone_name = Column(String(50))
    color = Column(String(50))

    __mapper_args__ = {"polymorphic_identity": "zone"}
