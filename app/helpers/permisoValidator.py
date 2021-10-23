from app.models.user import User
from app.models.permiso import Permiso
from sqlalchemy import and_

def permisoChercker(session, permiso):
    user = User.query.join(Permiso, Permiso.name == "user_index").filter(and_(User.roles.any(id=Permiso.id), User.email==session.get("user"))).first()
    if user:
        return True 