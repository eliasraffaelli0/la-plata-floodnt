import csv
from flask import redirect, render_template, request, url_for, session, abort
from app.helpers.auth import authenticated
from app.models.zone import Zone
from app.models.zone_coordinate import ZoneCoordinate
from app.db import db


def index():
    if not authenticated(session):
        abort(401)

    return render_template("zonas/index.html")


def upload_file():
    zone_file = request.files["zone_file"]
    zone_string = zone_file.read().decode("utf-8")

    zone_list = [
        {k: v for k, v in row.items()}
        for row in csv.DictReader(zone_string.splitlines(), skipinitialspace=True)
    ]

    # kk = (
    #     zone_list[0]["area"]
    #     .replace("],[", " ")
    #     .replace("[", " ")
    #     .replace("]", " ")
    #     .split()
    # )

    # import pdb

    # pdb.set_trace()
    ZoneCoordinate.query.delete()
    Zone.query.delete()

    for zona_inundada in zone_list:
        new_zona = Zone()
        new_zona.name = zona_inundada["name"]
        db.session.add(new_zona)
        db.session.commit()
        coordinate_list = (
            zona_inundada["area"]
            .replace("],[", " ")
            .replace("[", " ")
            .replace("]", " ")
            .split()
        )
        for coordinate_par in coordinate_list:
            coordinate_para = coordinate_par.replace(",", " ").split()
            new_coordinate = ZoneCoordinate()
            new_coordinate.zone_id = new_zona.id
            new_coordinate.latitude = coordinate_para[0]
            new_coordinate.longitude = coordinate_para[1]
            db.session.add(new_coordinate)
            db.session.commit()

    return render_template("zonas/index.html")
