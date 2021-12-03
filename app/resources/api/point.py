from flask import jsonify, Blueprint, request, g
from app.models.punto import Punto
from app.schema.point import point_pagination_schema, point_schema
from app.validators.puntoValidator import PuntoValidator
from app.db import db

point_api = Blueprint("puntos", __name__, url_prefix="/puntos")


@point_api.get("/")
def index():
    # http://127.0.0.1:5000/api/puntos/?page=1

    page = int(request.args.get("page", 1))
    # hacer query con un filter imagino?
    point_page = Punto.query.paginate(page=page, per_page=g.config.elementos_por_pagina)

    points = point_pagination_schema.dump(point_page)

    return jsonify(points)


@point_api.post("/")
def create():
    new_point = Punto(**request.get_json(force=True))
    errors = PuntoValidator(new_point).validate_create()

    if errors:
        response = errors
    else:
        db.session.add(new_point)
        db.session.commit()
        response = point_schema.dump(new_point)

    return jsonify(response)
