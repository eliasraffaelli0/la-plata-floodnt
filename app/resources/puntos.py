from flask import redirect, render_template, request, url_for, session, abort, flash
from app.db import db
from app.helpers.auth import authenticated
from app.models.punto import Punto
from app.validators.puntoDuplicateValidator import puntoDuplicateChecker
import re

def index():

    puntos = Punto.query.all()
    return render_template("puntos/index.html", puntos=puntos)

def new():

    return render_template("puntos/new.html")



def create():
    if not authenticated(session):
        abort(401)

    new_punto = Punto(**request.form)

    #raw string utilizado para validar que se trate de un mail
    regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+.[A-Z|a-z]{2,}\b'
    if not (re.fullmatch(regex, new_punto.email)):
        flash("Ingrese un mail válido.")
        return redirect(url_for("puntos_new")) 

 

    if puntoDuplicateChecker(Punto.name, new_punto.name, 'nombre'):
        return redirect(url_for("puntos_new"))

    if puntoDuplicateChecker(Punto.coordenadas, new_punto.coordenadas, 'coordenadas'):
        return redirect(url_for("puntos_new"))


    if (new_punto.name== '' or new_punto.direccion=='' or new_punto.coordenadas=='' 
    or new_punto.telefono=='' 
    or new_punto.email==''):
        flash("Debe completar todos los campos")
        return redirect(url_for("puntos_new"))



    db.session.add(new_punto)
    db.session.commit()
    return redirect(url_for("puntos_index"))



