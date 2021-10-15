import bcrypt
from flask import redirect, render_template, request, url_for, session, abort, flash
from app.models.user import User
from app.helpers.auth import authenticated
from app.db import db

# Protected resources
def index():
    if not authenticated(session):
        abort(401)

    users = User.query.all()
    return render_template("user/index.html", users=users)


def new():
    if not authenticated(session):
        abort(401)

    return render_template("user/new.html")


def create():
    if not authenticated(session):
        abort(401)
    
    new_user = User(**request.form)
    user = User.query.filter(User.email == new_user.email).first()
    if user:
        flash("El mail ya está registrado.")
        return redirect(url_for("user_new"))

    user = User.query.filter(User.username == new_user.username).first()
    if user:
        flash("El username ya está registrado.")
        return redirect(url_for("user_new"))    

    if new_user.email== '' or new_user.username=='' or new_user.password=='' or new_user.first_name=='' or new_user.last_name=='':
        flash("Debe completar todos los campos")
        return redirect(url_for("user_new"))
    
    #hasheo de la contraseña
    salt = bcrypt.gensalt()
    new_user.password = bcrypt.hashpw(new_user.password.encode(), salt)

    db.session.add(new_user)
    db.session.commit()
    return redirect(url_for("user_index"))
