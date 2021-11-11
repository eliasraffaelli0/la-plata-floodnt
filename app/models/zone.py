from sqlalchemy import Column, Integer, String, ForeignKey
from app.db import db


class Zone(db.Model):
    __tablename__ = "zone"
    id = Column(Integer, ForeignKey("point_group.id"), primary_key=True)
    zone_name = Column(String(50))
    color = Column(String(50))

    __mapper_args__ = {"polymorphic_identity": "zone"}
