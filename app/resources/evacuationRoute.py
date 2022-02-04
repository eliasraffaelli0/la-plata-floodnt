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
    params = request.args
    routes = EvacuationRoute.query
    if params.get("name", False):
        routes = routes.filter(EvacuationRoute.name == params["name"])

    if params.get("state", False):
        routes = routes.filter(EvacuationRoute.state == params["state"])

    routes = routes.order_by(
        text(f"created_at {g.config.criterio_de_ordenacion}")
    ).paginate(per_page=g.config.elementos_por_pagina)
    errors = {}
    return render_template(
        "evacuationRoute/index.html", errors=errors, fieldsInfo=params, routes=routes
    )


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
    """ Se transforma el diccionario inmutable en el que vienen almacenadas las coordenadas
    a un diccionario mutable y se guardan por separados en los campos de longitud y latitud para
    mandarlo al punto nuevo"""

    latLng = json.loads(request.form["coordinates"])
    new_evacuationRoute = EvacuationRoute()
    new_evacuationRoute.name = request.form["name"]
    new_evacuationRoute.description = request.form["description"]
    new_evacuationRoute.state = request.form["state"]
    errors = EvacuationRouteValidator(new_evacuationRoute).validate_create()
    if errors:
        return render_template(
            "evacuationRoute/new.html", errors=errors, fieldsInfo=new_evacuationRoute
        )
    for coor in latLng:
        new_punto = EvacuationRouteCoordinate()
        new_punto.latitude = coor["lat"]
        new_punto.longitude = coor["lng"]
        new_punto.evacuation_route_id = new_evacuationRoute.id
        new_evacuationRoute.coordinates.append(new_punto)
    db.session.add(new_evacuationRoute)
    db.session.commit()
    return redirect(url_for("evacuationRoute_index"))


def edit(id):
    if not authenticated(session):
        abort(401)

    route = EvacuationRoute.query.filter(EvacuationRoute.id == id).first()
    coords = list()
    """Creo una lista de diccionarios que tienen los pares de coordenadas de cada punto del recorrido
    que se pasa por parámetro a la vista """
    for point in route.coordinates:
        coordinatePair = dict()
        coordinatePair["lat"] = point.latitude
        coordinatePair["lng"] = point.longitude
        coords.append(coordinatePair)
    errors = {}
    return render_template(
        "evacuationRoute/edit.html",
        id=route.id,
        errors=errors,
        fieldsInfo=route,
        routeCoordinates=coords,
    )


def editInfo(id):
    if not authenticated(session):
        abort(401)
    """Transformo el campo coordinates a una lista, creo un nuevo recorrido, le asigno los valores 
    traídos del formulario y chequeo si son válidos, si son válidos, borro las coordenadas anteriores
    de la base de datos, creo las nuevas y las asigno al recorrido."""
    latLng = json.loads(request.form["coordinates"])
    route = EvacuationRoute.query.filter(EvacuationRoute.id == id).first()
    new_evacuationRoute = EvacuationRoute()
    new_evacuationRoute.name = request.form["name"]
    new_evacuationRoute.description = request.form["description"]
    new_evacuationRoute.state = request.form["state"]
    errors = EvacuationRouteValidator(new_evacuationRoute, route).validate_update()
    if errors:
        return render_template(
            "evacuationRoute/edit.html",
            errors=errors,
            id=route.id,
            fieldsInfo=new_evacuationRoute,
        )
    EvacuationRouteCoordinate.query.filter(
        EvacuationRouteCoordinate.evacuation_route_id == route.id
    ).delete()
    for coor in latLng:
        new_punto = EvacuationRouteCoordinate()
        new_punto.latitude = coor["lat"]
        new_punto.longitude = coor["lng"]
        new_punto.evacuation_route_id = route.id
        route.coordinates.append(new_punto)
    route.name = new_evacuationRoute.name
    route.description = new_evacuationRoute.description
    route.state = new_evacuationRoute.state
    db.session.commit()
    return redirect(url_for("evacuationRoute_index"))


def delete(id):
    if not authenticated(session):
        abort(401)

    """Elimino primero todas las coordenadas y después el recorrido"""

    route = EvacuationRoute.query.filter(EvacuationRoute.id == id).first()
    coordinates = EvacuationRouteCoordinate.query.filter(
        EvacuationRouteCoordinate.evacuation_route_id == id
    ).all()
    for coor in coordinates:
        db.session.delete(coor)
    db.session.delete(route)
    db.session.commit()
    return redirect(url_for("evacuationRoute_index"))
