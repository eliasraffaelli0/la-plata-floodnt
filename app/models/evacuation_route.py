# from sqlalchemy import Column, Integer, String, ForeignKey
# from app.db import db


# class Evacuation_route(db.Model):
#     __tablename__ = "evacuation_route"
#     id = Column(Integer, ForeignKey("point_group.id"), primary_key=True)
#     evacuation_route_name = Column(String(50))

#     __mapper_args__ = {"polymorphic_identity": "evacuation_route"}
