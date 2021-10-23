import bcrypt, re
from flask import redirect, render_template, request, url_for, session, abort, flash
from app.models.user import User
from app.helpers.auth import authenticated
from app.helpers.permisoValidator import permisoChecker
from app.db import db
from app.validators.userDuplicateValidator import userDuplicateChecker
from sqlalchemy import and_

# Protected resources
def index():
    if not authenticated(session):
        abort(401)
    if not permisoChecker(session, 'user_index'):
        abort(401)
    users = User.query.all()
    return render_template("user/index.html", users=users)


def new():
    if not authenticated(session):
        abort(401)
    if not permisoChecker(session, 'user_index'):
        abort(401)

    return render_template("user/new.html")


def create():
    if not authenticated(session):
        abort(401)
    
    new_user = User(**request.form)

    #raw string utilizado para validar que se trate de un mail
    regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
    if not (re.fullmatch(regex, new_user.email)):
        flash("Ingrese un mail válido.")
        return redirect(url_for("user_new"))

    if userDuplicateChecker(User.email, new_user.email, 'mail'):
        return redirect(url_for("user_new"))

    if userDuplicateChecker(User.username, new_user.username, 'username'):
        return redirect(url_for("user_new"))

    if new_user.email== '' or new_user.username=='' or new_user.password=='' or new_user.first_name=='' or new_user.last_name=='':
        flash("Debe completar todos los campos")
        return redirect(url_for("user_new"))
    
    #hasheo de la contraseña
    salt = bcrypt.gensalt()
    new_user.salt = salt
    new_user.password = bcrypt.hashpw(new_user.password.encode(), salt)

    db.session.add(new_user)
    db.session.commit()
    return redirect(url_for("user_index"))

def update_estado(username):
    params = User(**request.form)
    user = User.query.filter(User.username == username).first()
    user.activo = params.activo
    db.session.commit() 
    return redirect(url_for("user_index"))

def filter():
    params = User(**request.form)
    if params.first_name:
        users = User.query.filter(and_(User.first_name == params.first_name, User.activo == params.activo))
    else:
        users = User.query.filter(User.activo == params.activo)

    return render_template("user/index.html", users=users)