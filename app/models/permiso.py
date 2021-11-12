from sqlalchemy import Column, Integer, String
from app.db import db


class Permiso(db.Model):
    __tablename__ = "permisos"
    id = Column(Integer, primary_key=True)
    name = Column(String(30), unique=True)
