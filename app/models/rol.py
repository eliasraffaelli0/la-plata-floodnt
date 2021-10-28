from sqlalchemy import Column, Integer, String, ForeignKey
from app.db import db
from sqlalchemy.orm import relationship
from app.models.permiso import Permiso

association_table = db.Table(
    "rol_tiene_permiso",
    db.metadata,
    Column("rol_id", ForeignKey("roles.id"), primary_key=True),
    Column("permiso_id", ForeignKey("permisos.id"), primary_key=True),
)


class Rol(db.Model):
    __tablename__ = "roles"
    id = Column(Integer, primary_key=True)
    name = Column(String(30), unique=True)
    permisos = relationship(Permiso, secondary=association_table, backref="roless")

    def __init__(self, name=None):
        self.name = name
