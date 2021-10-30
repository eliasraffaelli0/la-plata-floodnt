import bcrypt
from flask import redirect, render_template, request, url_for, abort, session, flash
from app.models.configuracion import Configuracion
from app.models.user import User
from sqlalchemy import and_
from flask import g


def login():
    return render_template("auth/login.html")


def authenticate():
    params = request.form
    user = User.query.filter(User.email == params["email"]).first()
    config = Configuracion.query.first()
    if not user:
        flash("Usuario incorrecto.")
        return redirect(url_for("home"))

    # hasheo la contraseña y la comparo con la que está en la base de datos
    user_pass = bcrypt.hashpw(params["password"].encode(), user.salt.encode())
    user = User.query.filter(
        and_(User.email == params["email"], User.password == user_pass, User.activo)
    ).first()

    if not user:
        flash("Clave incorrecta o usuario inactivo")
        return redirect(url_for("home"))
    g.config = config
    # session["config"] = config
    session["user"] = user.email
    session["username"] = user.username
    flash("La sesión se inició correctamente.")
    return redirect(url_for("home"))


def logout():
    del session["user"]
    session.clear()
    flash("La sesión se cerró correctamente.")

    return redirect(url_for("home"))
