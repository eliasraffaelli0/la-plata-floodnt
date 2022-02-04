from flask import redirect, render_template, request, url_for, session, abort, flash
from sqlalchemy.sql.expression import false
from app.db import db
from app.helpers.auth import authenticated
from app.helpers.permisoValidator import permisoChecker
from app.models.configuracion import Configuracion


def index():
    if not authenticated(session):
        abort(401)
    if not permisoChecker(session, "config_index"):
        abort(401)
    return render_template("configuracion/configuracion.html")


def update():

    if not authenticated(session):
        abort(401)
    params = Configuracion(**request.form)
    if int(params.elementos_por_pagina) < 1:
        return redirect(url_for("configuracion_index"))
    configuracion = Configuracion.query.first()
    configuracion.elementos_por_pagina = params.elementos_por_pagina
    configuracion.tema_publico = params.tema_publico
    configuracion.tema_privado = params.tema_privado
    configuracion.criterio_de_ordenacion = params.criterio_de_ordenacion
    db.session.commit()
    return redirect(url_for("configuracion_index"))
