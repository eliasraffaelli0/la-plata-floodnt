from flask import redirect, render_template, request, url_for, session, abort, g
from app.helpers.auth import authenticated
from app.models.tracing import Tracing
from app.models.report import Report
from app.models.user import User
from app.db import db
from app.helpers.permisoValidator import permisoChecker
from app.validators.tracingValidator import TracingValidator
from sqlalchemy.sql import text, and_
import json


def new(id):
    if not authenticated(session):
        abort(401)
    if not permisoChecker(session, "user_index"):
        abort(401)
    errors = {}
    users = User.query
    report = Report.query.filter(Report.id == id).first()
    return render_template(
        "tracing/new.html", errors=errors, users=users, report=report
    )


def create(id):
    if not authenticated(session):
        abort(401)
    """ Se transforma el diccionario inmutable en el que vienen almacenado el estado del recorrido
     a un diccionario mutable, se almacena en una variable para poder eliminarlo del diccionario
     y poder crear el seguimiento sin problemas, ya que el estado no es un campo de los seguimientos"""
    params = request.form.to_dict()
    state = params["state"]
    del params["state"]
    new_tracing = Tracing(**params)
    errors = TracingValidator(new_tracing).validate_create()
    if errors:
        return render_template(
            "tracing/new.html",
            errors=errors,
            fieldsInfo=new_tracing,
        )
    user = User.query.filter(User.id == new_tracing.author_id).first()
    report = Report.query.filter(Report.id == id).first()
    new_tracing.report_id = id
    new_tracing.author = user
    new_tracing.report = report
    report.state = state
    db.session.add(new_tracing)
    db.session.commit()
    return redirect(url_for("reports_index"))
