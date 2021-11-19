import csv, uuid
from flask import render_template, request, session, abort
from app.helpers.auth import authenticated
from app.models.zone import Zone
from app.models.zone_coordinate import ZoneCoordinate
from app.db import db


def index():
    if not authenticated(session):
        abort(401)

    errors = {}
    return render_template("zonas/index.html", errors=errors)


def upload_file():
    zone_file = request.files["zone_file"]
    zone_string = zone_file.read().decode("utf-8")

    """Para obtener una lista de zonas inundadas lo que hago es dividir el string en una lista delimitado por los saltos de lineas.
    A cada item de la lista lo mapeo con DictReader para transformarlo en diccionario. Y finalmente armo la lista final donde cada 
    item es un diccionario que contiene la info de cada zona"""
    zone_list = [
        {k: v for k, v in row.items()}
        for row in csv.DictReader(zone_string.splitlines(), skipinitialspace=True)
    ]

    errors = {}
    """valido que tenga los campos correctos"""
    if not "name" in zone_list[0] or not "area" in zone_list[0]:
        errors["file"] = "Ingrese un archivo con el formato de area|coordenadas"
        return render_template("zonas/index.html", errors=errors)

    for zona_inundada in zone_list:
        new_zona = Zone()
        new_zona.name = zona_inundada["name"]
        """genero un string random para el codigo de cada zona"""
        new_zona.zone_code = str(uuid.uuid1())
        new_zona.color = "#b74848"
        new_zona.state = 0
        """si la zona ya está registrada elimino las coordenadas que tiene y las reemplazo por las que tiene el csv"""
        zone_is_registered = Zone.query.filter(Zone.name == new_zona.name).first()
        if zone_is_registered:
            ZoneCoordinate.query.filter(
                ZoneCoordinate.zone_id == zone_is_registered.id
            ).delete()
            db.session.commit()

        """quito los corchetes y hago una lista solo string de par de coordenadas separados por una coma.
        por ejemplo '-35.12234124,-43.34235256"""
        coordinate_list = (
            zona_inundada["area"]
            .replace("],[", " ")
            .replace("[", " ")
            .replace("]", " ")
            .split()
        )
        for coordinate_par in coordinate_list:
            """separo el string en una lista de dos items para obtener el valor de la latitud y la longitud"""
            coordinate_para = coordinate_par.replace(",", " ").split()
            new_coordinate = ZoneCoordinate()
            new_coordinate.latitude = coordinate_para[0]
            new_coordinate.longitude = coordinate_para[1]
            """si la zona ya está registrada le hago un append, sino lo hago en la zona nueva"""
            if zone_is_registered:
                zone_is_registered.coordinates.append(new_coordinate)
            else:
                new_zona.coordinates.append(new_coordinate)
        """si la zona no está registrada la añade a la db, sino solo hace el commit ya que la zona ya estaría registrada"""
        if not zone_is_registered:
            db.session.add(new_zona)
        db.session.commit()
    # es una chanchada pero tiempos desesperados requieren medidas desesperadas

    return render_template("zonas/index.html", errors=errors)
