from flask import redirect, render_template, request, url_for, session, abort
from app.db import db
from app.helpers.auth import authenticated
from app.models.punto import Punto

def index():

    puntos = Punto.query.all()
    return render_template("puntos/index.html", puntos=puntos)

def new():

    return render_template("puntos/new.html")


def create():

    new_punto = Punto(**request.form)
    db.session.add(new_punto)
    db.session.commit()

    return redirect(url_for("puntos_index"))