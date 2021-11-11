from app.models.user import User
from app.models.permiso import Permiso
from app.models.rol import Rol
from sqlalchemy import and_


def permisoChecker(session, permiso):
    user = User.query.filter(User.email == session.get("user")).first()
    if permiso in user.permisos():
        return True
