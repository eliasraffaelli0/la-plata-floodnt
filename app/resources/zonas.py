import csv
from flask import render_template, request, session, abort
from app.helpers.auth import authenticated
from app.models.zone import Zone
from app.models.zone_coordinate import ZoneCoordinate
from app.validators.zoneValidator import ZoneValidator
from app.db import db


def index():
    if not authenticated(session):
        abort(401)

    return render_template("zonas/index.html")


def upload_file():
    zone_file = request.files["zone_file"]
    zone_string = zone_file.read().decode("utf-8")

    # validar por comlumnas name y coordenadas
    # append y add commit al final
    # codigo de zona (usar uuid)
    # explicar como haría para actualizar las tabals
    # explicar lo que pedía el enunciado, lo que hice y cómo lo solucionaría

    """Para obtener una lista de zonas inundadas lo que hago es dividir el string en una lista delimitado por los saltos de lineas.
    A cada item de la lista lo mapeo con DictReader para transformarlo en diccionario. Y finalmente armo la lista final donde cada 
    item es un diccionario que contiene la info de cada zona"""
    zone_list = [
        {k: v for k, v in row.items()}
        for row in csv.DictReader(zone_string.splitlines(), skipinitialspace=True)
    ]

    """vacío la tabla antes de volver a llenarla con los datos del archivo"""

    for zona_inundada in zone_list:
        new_zona = Zone()
        new_zona.name = zona_inundada["name"]
        kk = ZoneValidator(new_zona).validate_username()

        """comiteo primero la zona para que le quede asignado un id para luego pasarselo a cada par de coordenadas"""
        # db.session.add(new_zona)
        # db.session.commit()
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
            # new_coordinate.zone_id = new_zona.id
            new_coordinate.latitude = coordinate_para[0]
            new_coordinate.longitude = coordinate_para[1]
            new_zona.coordinates.append(new_coordinate)
            # db.session.add(new_coordinate)
            # db.session.commit()
        db.session.add(new_zona)
        db.session.commit()
    # es una chanchada pero tiempos desesperados requieren medidas desesperadas

    return render_template("zonas/index.html")
