from flask import redirect, render_template, request, url_for, session, abort, g
from app.db import db
from app.helpers.auth import authenticated
from app.models.punto import Punto
from app.validators.puntoValidator import PuntoValidator
from app.helpers.permisoValidator import permisoChecker
from sqlalchemy.sql import text, and_
import json


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
    # para el controlador de zona hay que hacer el load para transformarlo a un arreglo de diccionarios
    """ Se transforma el diccionario inmutable en el que vienen almacenadas las coordenadas
     a un diccionario mutable y se guardan por separados en los campos de longitud y latitud para
     mandarlo al punto nuevo"""
    latLng = json.loads(request.form["coordinates"])
    params = request.form.to_dict()
    del params["coordinates"]
    params["latitude"] = latLng["lat"]
    params["longitude"] = latLng["lng"]
    new_punto = Punto(**params)
    errors = PuntoValidator(new_punto).validate_create()
    if errors:
        return render_template("puntos/new.html", errors=errors, fieldsInfo=new_punto)
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


def edit(id):
    if not authenticated(session):
        abort(401)

    punto = Punto.query.filter(Punto.id == id).first()
    errors = {}
    return render_template(
        "puntos/edit.html", id=punto.id, errors=errors, fieldsInfo=punto
    )


def editInfo(id):
    if not authenticated(session):
        abort(401)

    latLng = json.loads(request.form["coordinates"])
    params = request.form.to_dict()
    del params["coordinates"]
    params["latitude"] = latLng["lat"]
    params["longitude"] = latLng["lng"]
    punto = Punto.query.filter(Punto.id == id).first()
    new_punto = Punto(**params)
    errors = PuntoValidator(new_punto, punto).validate_update()

    if errors:
        return render_template(
            "puntos/edit.html",
            errors=errors,
            id=punto.id,
            fieldsInfo=new_punto,
        )
    punto.email = new_punto.email
    punto.name = new_punto.name
    punto.address = new_punto.address
    punto.state = new_punto.state
    punto.telephone = new_punto.telephone
    db.session.commit()
    return redirect(url_for("puntos_index"))


def delete(id):
    if not authenticated(session):
        abort(401)
    punto = Punto.query.filter(Punto.id == id).first()
    db.session.delete(punto)
    db.session.commit()
    return redirect(url_for("puntos_index"))
