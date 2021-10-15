from flask import redirect, render_template, request, url_for, session, abort
from app.helpers.auth import authenticated
from app.models.punto import Punto

def index():
    if not authenticated(session):
        abort(401)

    puntos = User.query.all()
    return render_template("puntos/index.html", users=puntos)

def new():
    if not authenticated(session):
        abort(401)

    return render_template("puntos/new.html")


def create():
    if not authenticated(session):
        abort(401)

    return redirect(url_for("puntos_index"))