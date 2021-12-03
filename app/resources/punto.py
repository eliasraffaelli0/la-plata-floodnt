from flask import redirect, render_template, request, url_for, session, abort, g
from app.db import db
from app.helpers.auth import authenticated
from app.models.punto import Punto
from app.validators.puntoValidator import PuntoValidator
from app.helpers.permisoValidator import permisoChecker
from sqlalchemy.sql import text, and_
import json


def index():
    """Accedo a la variable de configuracion del g object, pagino por la cantidad de
    elementos que tenga almacenada en esa variable y ordeno por el criterio"""
    if not authenticated(session):
        abort(401)
    params = request.args
    puntos = Punto.query
    if params.get("name", False):
        puntos = puntos.filter(Punto.name == params["name"])

    if params.get("state", False):
        puntos = puntos.filter(Punto.state == params["state"])

    puntos = puntos.order_by(
        text(f"created_at {g.config.criterio_de_ordenacion}")
    ).paginate(per_page=g.config.elementos_por_pagina)
    errors = {}

    return render_template(
        "puntos/index.html", puntos=puntos, fieldsInfo=params, errors=errors
    )


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
    new_punto = Punto(**params)
    punto = Punto.query.filter(Punto.id == id).first()
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
    punto.latitude = new_punto.latitude
    punto.longitude = new_punto.longitude
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
