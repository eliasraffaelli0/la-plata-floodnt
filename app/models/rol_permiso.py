from app.db import db
from app.models.permiso import Permiso
from app.models.rol import Rol
from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.orm import relationship

class RolPermiso(db.Model):
    __tablename__= "rol_tiene_permiso"
    id = Column(Integer, primary_key=True)
    rol_id = Column(Integer, ForeignKey("roles.id"))
    rol = relationship(Rol)
    permiso_id = Column(Integer, ForeignKey("permisos.id"))
    permiso = relationship(Permiso)

    def __init__(self, rol_id=None, permiso_id=None):
        self.rol_id = rol_id
        self.permiso_id = permiso_id