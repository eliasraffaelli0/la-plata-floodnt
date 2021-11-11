from flask import redirect, render_template, request, url_for, session, abort, g
from app.helpers.auth import authenticated
from app.models.evacuation_route import Evacuation_route
from app.db import db
from app.helpers.permisoValidator import permisoChecker
from app.validators.evacuationRouteValidator import Evacuation_route_validator
from sqlalchemy.sql import text, and_
import json


def index():
    if not authenticated(session):
        abort(401)

    """Accedo a la variable de configuracion del g object, pagino por la cantidad de
    elementos que tenga almacenada en esa variable y ordeno por el criterio"""
    if g.config.criterio_de_ordenacion == "asc":

        routes = Evacuation_route.query.order_by(
            Evacuation_route.created_at.asc()
        ).paginate(per_page=g.config.elementos_por_pagina)

    elif g.config.criterio_de_ordenacion == "desc":
        routes = Evacuation_route.query.order_by(
            Evacuation_route.created_at.desc()
        ).paginate(per_page=g.config.elementos_por_pagina)

    return render_template("evacuation_route/index.html")


def new():
    if not authenticated(session):
        abort(401)
    if not permisoChecker(session, "user_index"):
        abort(401)
    errors = {}
    return render_template("evacuation_route/new.html", errors=errors)


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
    new_route = Evacuation_route(**params)
    errors = Evacuation_route_validator(new_route).validate_create()
    if errors:
        return render_template(
            "evacuation_route/new.html", errors=errors, fieldsInfo=new_route
        )
    db.session.add(new_route)
    db.session.commit()
    return redirect(url_for("evacuation_route_index"))


def filter():
    params = Evacuation_route(**request.form)
    if params.name and not params.state:
        routes = (
            Evacuation_route.query.filter(Evacuation_route.name == params.name)
            .order_by(text(f"created_at {g.config.criterio_de_ordenacion}"))
            .paginate(per_page=g.config.elementos_por_pagina)
        )
    elif params.state and not params.name:
        routes = (
            Evacuation_route.query.filter(Evacuation_route.state == params.state)
            .order_by(text(f"created_at {g.config.criterio_de_ordenacion}"))
            .paginate(per_page=g.config.elementos_por_pagina)
        )
    else:
        routes = (
            Evacuation_route.query.filter(
                and_(
                    Evacuation_route.name == params.name,
                    Evacuation_route.state == params.state,
                )
            )
            .order_by(text(f"created_at {g.config.criterio_de_ordenacion}"))
            .paginate(per_page=g.config.elementos_por_pagina)
        )

    return render_template("evacuation_route/index.html", routes=routes)


def edit(id):
    if not authenticated(session):
        abort(401)

    route = Evacuation_route.query.filter(Evacuation_route.id == id).first()
    errors = {}
    return render_template(
        "evacuation_route/edit.html", id=route.id, errors=errors, fieldsInfo=route
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
    route = Evacuation_route.query.filter(Evacuation_route.id == id).first()
    db.session.delete(route)
    db.session.commit()
    return redirect(url_for("evacuation_route_index"))
