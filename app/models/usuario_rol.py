from app.db import db
from app.models.user import User
from app.models.rol import Rol
from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.orm import relationship

class UserRol(db.Model):
    __tablename__= "usuario_tiene_rol"
    id = Column(Integer, primary_key=True)
    usuario_id = Column(Integer, ForeignKey("usuarios.id"))
    usuario = relationship(User)
    rol_id = Column(Integer, ForeignKey("roles.id"))
    rol = relationship(Rol)

    def __init__(self, usuario_id=None, rol_id=None):
        self.usuario_id = usuario_id
        self.rol_id = rol_id