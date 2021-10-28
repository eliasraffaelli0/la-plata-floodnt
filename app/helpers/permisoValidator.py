from app.models.user import User
from app.models.permiso import Permiso
from app.models.rol import Rol
from sqlalchemy import and_


def permisoChecker(session, permiso):
    user = (
        User.query.join(Permiso, Permiso.name == permiso)
        .filter(
            and_(
                User.roless.any(Rol.id == Permiso.id), User.email == session.get("user")
            )
        )
        .first()
    )
    if user:
        return True
