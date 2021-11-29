from flask import jsonify, Blueprint
from app.models.zone import Zone
from app.models.user import User

zone_api = Blueprint("consultas", __name__, url_prefix="/consultas")


@zone_api.get("/")
def index():
    zone_rows = Zone.query.all()
    print(zone_rows)
    zones = [zone.as_dict() for zone in zone_rows]

    return jsonify(zones=zones)
