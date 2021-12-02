from flask import jsonify, Blueprint, request
from app.models.zone import Zone
from app.schema.zone import ZoneSchema

zone_api = Blueprint("consultas", __name__, url_prefix="/consultas")


@zone_api.get("/")
def index():
    zone_rows = Zone.query.all()
    print(zone_rows)
    zones = [zone.as_dict() for zone in zone_rows]

    return jsonify(zones=zones)


@zone_api.post("/")
def create():
    data = request.get_json(force=True)
    return jsonify(ZoneSchema.dump(data))
