from flask import redirect, render_template, request, url_for, session, abort, g
from app.helpers.auth import authenticated
from app.models.evacuationRouteCoordinates import EvacuationRouteCoordinate
from app.models.evacuationRoute import EvacuationRoute
from app.db import db
from app.helpers.permisoValidator import permisoChecker
from app.validators.evacuationRouteValidator import EvacuationRouteValidator
from sqlalchemy.sql import text, and_
import json


def index():
    if not authenticated(session):
        abort(401)

    """Accedo a la variable de configuracion del g object, pagino por la cantidad de
    elementos que tenga almacenada en esa variable y ordeno por el criterio"""
    if g.config.criterio_de_ordenacion == "asc":

        routes = EvacuationRoute.query.order_by(
            EvacuationRoute.created_at.asc()
        ).paginate(per_page=g.config.elementos_por_pagina)

    elif g.config.criterio_de_ordenacion == "desc":
        routes = EvacuationRoute.query.order_by(
            EvacuationRoute.created_at.desc()
        ).paginate(per_page=g.config.elementos_por_pagina)

    return render_template("evacuationRoute/index.html", routes=routes)


def new():
    if not authenticated(session):
        abort(401)
    if not permisoChecker(session, "user_index"):
        abort(401)
    errors = {}
    return render_template("evacuationRoute/new.html", errors=errors)


def create():
    if not authenticated(session):
        abort(401)
    # para el controlador de zona hay que hacer el load para transformarlo a un arreglo de diccionarios
    """ Se transforma el diccionario inmutable en el que vienen almacenadas las coordenadas
     a un diccionario mutable y se guardan por separados en los campos de longitud y latitud para
     mandarlo al punto nuevo"""

    latLng = json.loads(request.form["coordinates"])
    import pdb

    new_evacuationRoute = EvacuationRoute()
    new_evacuationRoute.name = request.form["name"]
    new_evacuationRoute.description = request.form["description"]
    new_evacuationRoute.state = request.form["state"]
    errors = EvacuationRouteValidator(new_evacuationRoute).validate_create()
    if errors:
        return render_template(
            "evacuationRoute/new.html", errors=errors, fieldsInfo=new_evacuationRoute
        )
    db.session.add(new_evacuationRoute)
    db.session.commit()
    for coor in latLng:
        new_punto = EvacuationRouteCoordinate()
        new_punto.latitude = coor["lat"]
        new_punto.longitude = coor["lng"]
        new_punto.evacuation_route_id = new_evacuationRoute.id
        db.session.add(new_punto)
        db.session.commit()

    return redirect(url_for("evacuationRoute_index"))


def filter():
    params = EvacuationRoute(**request.form)
    if params.name and not params.state:
        routes = (
            EvacuationRoute.query.filter(EvacuationRoute.name == params.name)
            .order_by(text(f"created_at {g.config.criterio_de_ordenacion}"))
            .paginate(per_page=g.config.elementos_por_pagina)
        )
    elif params.state and not params.name:
        routes = (
            EvacuationRoute.query.filter(EvacuationRoute.state == params.state)
            .order_by(text(f"created_at {g.config.criterio_de_ordenacion}"))
            .paginate(per_page=g.config.elementos_por_pagina)
        )
    else:
        routes = (
            EvacuationRoute.query.filter(
                and_(
                    EvacuationRoute.name == params.name,
                    EvacuationRoute.state == params.state,
                )
            )
            .order_by(text(f"created_at {g.config.criterio_de_ordenacion}"))
            .paginate(per_page=g.config.elementos_por_pagina)
        )

    return render_template("evacuarionRoute/index.html", routes=routes)


# def edit(id):
#     if not authenticated(session):
#         abort(401)

#     route = EvacuationRoute.query.filter(EvacuationRoute.id == id).first()
#     errors = {}
#     return render_template(
#         "evacuationRoute/edit.html", id=route.id, errors=errors, fieldsInfo=route
#     )


# def editInfo(id):
#     if not authenticated(session):
#         abort(401)

#     latLng = json.loads(request.form["coordinates"])
#     params = request.form.to_dict()
#     del params["coordinates"]
#     params["latitude"] = latLng["lat"]
#     params["longitude"] = latLng["lng"]
#     punto = Punto.query.filter(Punto.id == id).first()
#     new_punto = Punto(**params)
#     errors = PuntoValidator(new_punto, punto).validate_update()

#     if errors:
#         return render_template(
#             "puntos/edit.html",
#             errors=errors,
#             id=punto.id,
#             fieldsInfo=new_punto,
#         )
#     punto.email = new_punto.email
#     punto.name = new_punto.name
#     punto.address = new_punto.address
#     punto.state = new_punto.state
#     punto.telephone = new_punto.telephone
#     db.session.commit()
#     return redirect(url_for("puntos_index"))


def delete(id):
    if not authenticated(session):
        abort(401)
    route = EvacuationRoute.query.filter(EvacuationRoute.id == id).first()
    coordinates = EvacuationRouteCoordinate.query.filter(
        EvacuationRouteCoordinate.evacuation_route_id == id
    ).all()
    for coor in coordinates:
        db.session.delete(coor)
    db.session.delete(route)
    db.session.commit()
    return redirect(url_for("evacuationRoute_index"))
