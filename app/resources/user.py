import bcrypt
from flask import redirect, render_template, request, url_for, session, abort, g
from app.models.user import User
from app.models.rol import Rol
from app.helpers.auth import authenticated
from app.helpers.permisoValidator import permisoChecker
from app.db import db
from app.validators.userValidator import UserValidator
from sqlalchemy import and_, text
from app.models.coordenate_group import Point_group, Zone, Evacuation_route
from app.models.coordenate import Coordenate
from sqlalchemy.orm import with_polymorphic

# Protected resources
def index():
    if not authenticated(session):
        abort(401)
    if not permisoChecker(session, "user_index"):
        abort(401)

    kk3 = Coordenate.query.all()
    kk0 = Point_group.query.all()
    kk = Evacuation_route.query.all()
    kk2 = Zone.query.all()

    users = User.query.order_by(
        text(f"created_at {g.config.criterio_de_ordenacion}")
    ).paginate(per_page=g.config.elementos_por_pagina)

    return render_template("user/index.html", users=users)


def new():
    if not authenticated(session):
        abort(401)
    if not permisoChecker(session, "user_new"):
        abort(401)
    errors = {}
    return render_template("user/new.html", errors=errors)


def create():
    if not authenticated(session):
        abort(401)
    if not permisoChecker(session, "user_new"):
        abort(401)

    new_user = User(**request.form)
    errors = {}
    errors = UserValidator(new_user).validate_create()

    if errors:
        return render_template("user/new.html", errors=errors, fieldsInfo=new_user)

    # hasheo de la contraseña
    salt = bcrypt.gensalt()
    new_user.salt = salt
    new_user.password = bcrypt.hashpw(new_user.password.encode(), salt)

    db.session.add(new_user)
    db.session.commit()
    return redirect(url_for("user_index"))


def filter():
    params = User(**request.form)
    if params.first_name and not params.activo:
        users = (
            User.query.filter(User.first_name == params.first_name)
            .order_by(text(f"created_at {g.config.criterio_de_ordenacion}"))
            .paginate(per_page=g.config.elementos_por_pagina)
        )
    elif params.activo and not params.first_name:
        users = (
            User.query.filter(User.activo == params.activo)
            .order_by(text(f"created_at {g.config.criterio_de_ordenacion}"))
            .paginate(per_page=g.config.elementos_por_pagina)
        )
    else:
        users = (
            User.query.filter(
                and_(User.first_name == params.first_name, User.activo == params.activo)
            )
            .order_by(text(f"created_at {g.config.criterio_de_ordenacion}"))
            .paginate(per_page=g.config.elementos_por_pagina)
        )

    return render_template("user/index.html", users=users)


def update_estado(username):
    params = User(**request.form)
    user = User.query.filter(User.username == username).first()
    user.activo = params.activo
    db.session.commit()
    return redirect(url_for("user_index"))


def edit(id):
    if not authenticated(session):
        abort(401)
    if not permisoChecker(session, "user_edit"):
        abort(401)

    user = User.query.filter(User.id == id).first()
    errors = {}
    return render_template(
        "user/edit.html", id=user.id, errors=errors, fieldsInfo=user, rolInfo=user.roles
    )


def editInfo(id):
    if not authenticated(session):
        abort(401)
    if not permisoChecker(session, "user_new"):
        abort(401)

    user = User.query.filter(User.id == id).first()
    new_user = User(**request.form)

    errors = UserValidator(new_user, user).validate_update()

    if errors:
        return render_template(
            "user/edit.html",
            errors=errors,
            id=user.id,
            fieldsInfo=new_user,
        )
    user.email = new_user.email
    user.username = new_user.username
    user.first_name = new_user.first_name
    user.last_name = new_user.last_name
    db.session.commit()
    return redirect(url_for("user_index"))


def editRol(id):
    if not authenticated(session):
        abort(401)
    if not permisoChecker(session, "user_edit_rol"):
        abort(401)

    user = User.query.filter(User.id == id).first()
    params = request.form.getlist("name")

    """Traigo los roles que tengan el mismo nombre que los que contiene params y se los agrego al usuario"""
    for param in params:
        rol = Rol.query.filter(Rol.name == param).first()
        user.roles.append(rol)

    """uso list comprehension para obtener los nombres de los roles que tiene el usuario, luego quito los que ya están en params.
    De esta forma verifico que en el formulario se le haya quitado un rol que el usuario tenía asignado.
    Luego de quedarme con los roles que el usuario ya no debería tener, hago un remove y se los quito de sus roles.
    no sé si es la forma más eficiente de hacer esto pero me sentí un hacker"""
    rolesARemover = list(set([x.name for x in user.roles]) - set(params))
    for rol in rolesARemover:
        user.roles.remove(Rol.query.filter(Rol.name == rol).first())

    db.session.commit()
    return redirect(url_for("user_index"))
