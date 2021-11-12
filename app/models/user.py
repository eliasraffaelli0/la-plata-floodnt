from sqlalchemy import Column, Integer, String, DateTime, Table, ForeignKey
from sqlalchemy.sql import func
from app.db import db
from sqlalchemy.orm import relationship
from app.models.rol import Rol


association_table = db.Table(
    "usuario_tiene_rol",
    db.metadata,
    Column("usuario_id", ForeignKey("usuarios.id"), primary_key=True),
    Column("rol_id", ForeignKey("roles.id"), primary_key=True),
)


class User(db.Model):
    __tablename__ = "usuarios"
    id = Column(Integer, primary_key=True)
    email = Column(String(30), unique=True)
    username = Column(String(30), unique=True)
    password = Column(String(255))
    salt = Column(String(255))
    activo = Column(Integer)
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    first_name = Column(String(30))
    last_name = Column(String(30))
    roles = relationship(Rol, secondary=association_table, backref="usuarios")

    # esto no va a quedar así eh, voy a volver vos
    def permisos(self):
        userRoles = []
        for rol in self.roles:
            for permiso in rol.permisos:
                userRoles.append(permiso.name)
        return userRoles
