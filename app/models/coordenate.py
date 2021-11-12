from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy import ForeignKey
from app.db import db
from app.models.coordenate_group import Point_group


class Coordenate(db.Model):
    __tablename__ = "coordenates"
    id = Column(Integer, primary_key=True)
    latitude = Column(String(50), unique=True)
    longitude = Column(String(50), unique=True)
    point_group_id = Column(ForeignKey("point_group.id"))
    point_group = relationship("Point_group", back_populates="coordenates")
