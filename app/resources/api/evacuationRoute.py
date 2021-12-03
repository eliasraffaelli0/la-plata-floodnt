from flask import jsonify, Blueprint, request, g
from app.models.evacuationRoute import EvacuationRoute
from app.schema.evacuationRouteSchema import evacuation_routes_pagination_schema
from app.db import db

evacuationRoute_api = Blueprint("recorridos", __name__, url_prefix="/recorridos")


@evacuationRoute_api.get("/")
def index():
    # http://127.0.0.1:5000/api/puntos/?page=1
    page = int(request.args.get("page", 1))
    route_page = EvacuationRoute.query.paginate(
        page=page, per_page=g.config.elementos_por_pagina
    )
    points = evacuation_routes_pagination_schema.dump(route_page)

    return jsonify(points)


# @point_api.post("/")
# def create():
#     new_point = Punto(**request.get_json(force=True))
#     errors = PuntoValidator(new_point).validate_create()

#     if errors:
#         response = errors
#     else:
#         db.session.add(new_point)
#         db.session.commit()
#         response = point_schema.dump(new_point)

#     return jsonify(response)
