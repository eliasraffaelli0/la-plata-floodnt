from flask import jsonify, Blueprint, request, g
from app.models.zone import Zone
from app.schema.zoneSchema import zone_pagination_schema, zone_schema

zone_api = Blueprint("zonas", __name__, url_prefix="/zonas")


@zone_api.get("/")
def index():
    # http://127.0.0.1:5000/api/zonas/?page=1
    page = int(request.args.get("page", 1))
    zone_page = Zone.query.paginate(page=page, per_page=g.config.elementos_por_pagina)
    zones = zone_pagination_schema.dump(zone_page)

    return jsonify(zones)


@zone_api.get("/id/")
def oneZone():
    # http://127.0.0.1:5000/api/zonas/id/?id=1
    id = int(request.args.get("id", 1))
    zone_query = Zone.query.filter(Zone.id == id).first()
    zone_dump = zone_schema.dump(zone_query)

    return jsonify(zone_dump)
