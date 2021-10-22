from sqlalchemy.sql.elements import and_
from app.models.user import User
from app.models.rol import Rol
from app.models.permiso import Permiso
from sqlalchemy import and_
# from app.models.usuario_rol import UserRol
# from app.models.rol_permiso import RolPermiso

def permisoChercker(session, permiso):
    # user = User.query.filter( User.id==userEmail, User.id == UserRol.usuario_id).filter(UserRol.rol_id == Rol.id).filter(Rol.name == rol).first() 
    # user = User.query.filter(and_(User.email==session.get("user"), User.id == UserRol.usuario_id, UserRol.rol_id == Rol.id, Rol.id == RolPermiso.rol_id, RolPermiso.permiso_id == Permiso.id, Permiso.name == permiso)).first() 
    permi = Permiso.query.filter(Permiso.name==permiso).first()
   
    if permi:
        user = User.query.filter(and_(User.roles.any(id=permi.id), User.email==session.get("user"))).first()
        if user:
            return True 