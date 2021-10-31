import bcrypt, re
from flask import redirect, render_template, request, url_for, session, abort, flash
from app.models.user import User
from app.helpers.auth import authenticated
from app.helpers.permisoValidator import permisoChecker
from app.db import db
from app.validators.userValidator import UserValidator
from sqlalchemy import and_

# Protected resources
def index():
    if not authenticated(session):
        abort(401)
    if not permisoChecker(session, "user_index"):
        abort(401)
    users = User.query.all()
    return render_template("user/index.html", users=users)


def new():
    if not authenticated(session):
        abort(401)
    if not permisoChecker(session, "user_index"):
        abort(401)
    errors = {}
    return render_template("user/new.html", errors=errors)


def create():
    if not authenticated(session):
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
    if params.first_name:
        users = User.query.filter(
            and_(User.first_name == params.first_name, User.activo == params.activo)
        )
    else:
        users = User.query.filter(User.activo == params.activo)

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

    user = User.query.filter(User.id == id).first()
    errors = {}
    return render_template("user/edit.html", id=user.id, errors=errors, fieldsInfo=user)


def editInfo(id):
    if not authenticated(session):
        abort(401)

    user = User.query.filter(User.id == id).first()
    new_user = User(**request.form)
    errors = {}
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
