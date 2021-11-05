from flask import redirect, render_template, request, url_for, session, abort, flash, g
from app.db import db
from app.helpers.auth import authenticated
from app.models.punto import Punto
from app.validators.puntoValidator import PuntoValidator
from app.helpers.permisoValidator import permisoChecker
from sqlalchemy.sql import text, and_
import re


def index():
    # Accedo a la variable de configuracion del g object, pagino por la cantidad de
    # elementos que tenga almacenada en esa variable y ordeno por el criterio
    if g.config.criterio_de_ordenacion == "asc":

        puntos = Punto.query.order_by(Punto.created_at.asc()).paginate(
            per_page=g.config.elementos_por_pagina
        )

    elif g.config.criterio_de_ordenacion == "desc":
        puntos = Punto.query.order_by(Punto.created_at.desc()).paginate(
            per_page=g.config.elementos_por_pagina
        )

    return render_template("puntos/index.html", puntos=puntos)


def new():
    if not authenticated(session):
        abort(401)
    if not permisoChecker(session, "user_index"):
        abort(401)
    errors = {}
    return render_template("puntos/new.html", errors=errors)


def create():
    if not authenticated(session):
        abort(401)

    new_punto = Punto(**request.form)
    errors = {}
    errors = PuntoValidator(new_punto).validate_create()

    if errors:
        return render_template("puntos/new.html", errors=errors, fieldsInfo=new_punto)

    if (
        new_punto.name == ""
        or new_punto.address == ""
        or new_punto.latitude == ""
        or new_punto.longitude == ""
        or new_punto.telephone == ""
        or new_punto.email == ""
    ):
        flash("Debe completar todos los campos")
        return redirect(url_for("puntos_new"))

    db.session.add(new_punto)
    db.session.commit()
    return redirect(url_for("puntos_index"))


def filter():
    params = Punto(**request.form)
    if params.name and not params.state:
        puntos = (
            Punto.query.filter(Punto.name == params.name)
            .order_by(text(f"created_at {g.config.criterio_de_ordenacion}"))
            .paginate(per_page=g.config.elementos_por_pagina)
        )
    elif params.state and not params.name:
        puntos = (
            Punto.query.filter(Punto.state == params.state)
            .order_by(text(f"created_at {g.config.criterio_de_ordenacion}"))
            .paginate(per_page=g.config.elementos_por_pagina)
        )
    else:
        puntos = (
            Punto.query.filter(
                and_(Punto.name == params.name, Punto.state == params.state)
            )
            .order_by(text(f"created_at {g.config.criterio_de_ordenacion}"))
            .paginate(per_page=g.config.elementos_por_pagina)
        )

    return render_template("puntos/index.html", puntos=puntos)
