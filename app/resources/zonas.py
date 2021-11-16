import csv
from flask import render_template, request, session, abort, g
from app.helpers.auth import authenticated
from app.models.zone import Zone
from app.models.zone_coordinate import ZoneCoordinate
from app.db import db


def index():
    if not authenticated(session):
        abort(401)

    # Accedo a la variable de configuracion del g object, pagino por la cantidad de
    # elementos que tenga almacenada en esa variable y ordeno por el criterio
    if g.config.criterio_de_ordenacion == "asc":

        zones = Zone.query.order_by(Zone.created_at.asc()).paginate(
            per_page=g.config.elementos_por_pagina
        )

    elif g.config.criterio_de_ordenacion == "desc":
        zones = Zone.query.order_by(Zone.created_at.desc()).paginate(
            per_page=g.config.elementos_por_pagina
        )

    return render_template("zonas/index.html", zones=zones)


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

    """vacío la tabla antes de volver a llenarla con los datos del archivo"""
    ZoneCoordinate.query.delete()
    Zone.query.delete()

    for zona_inundada in zone_list:
        new_zona = Zone()
        new_zona.name = zona_inundada["name"]
        new_zona.color = "#ff7800"
        new_zona.state = 0
        """comiteo primero la zona para que le quede asignado un id para luego pasarselo a cada par de coordenadas"""
        db.session.add(new_zona)
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
            new_coordinate.zone_id = new_zona.id
            new_coordinate.latitude = coordinate_para[0]
            new_coordinate.longitude = coordinate_para[1]
            db.session.add(new_coordinate)
            db.session.commit()
    # es una chanchada pero tiempos desesperados requieren medidas desesperadas

    return render_template("zonas/index.html")


def edit(id):
    if not authenticated(session):
        abort(401)

    zone = Zone.query.filter(Zone.id == id).first()
    errors = {}
    return render_template(
        "zonas/edit.html", id=punto.id, errors=errors, fieldsInfo=zone
    )


def delete(id):
    if not authenticated(session):
        abort(401)
    zone = Zone.query.filter(Zone.id == id).first()
    db.session.delete(zone)
    db.session.commit()
    return redirect(url_for("zonas_index"))
