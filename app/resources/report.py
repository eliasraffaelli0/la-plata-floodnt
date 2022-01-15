from flask import redirect, render_template, request, url_for, session, abort, g
from app.helpers.auth import authenticated
from app.models.report import Report
from app.db import db
from app.helpers.permisoValidator import permisoChecker
from app.validators.reportValidator import ReportValidator
from sqlalchemy.sql import text, and_
import json


def index():
    if not authenticated(session):
        abort(401)

    """Accedo a la variable de configuracion del g object, pagino por la cantidad de
    elementos que tenga almacenada en esa variable y ordeno por el criterio"""
    params = request.args
    reports = Report.query
    # import pdb

    # pdb.set_trace()
    if params.get("title", False):
        reports = reports.filter(Report.title == params["title"])

    if params.get("state", False):
        reports = reports.filter(Report.state == params["state"])

    # if params.get("date", False):
    #     report = reports.filter(Report.created_at == params["created_at"])
    reports = reports.order_by(
        text(f"created_at {g.config.criterio_de_ordenacion}")
    ).paginate(per_page=g.config.elementos_por_pagina)
    errors = {}
    return render_template(
        "report/index.html", errors=errors, fieldsInfo=params, reports=reports
    )


def new():
    if not authenticated(session):
        abort(401)
    if not permisoChecker(session, "user_index"):
        abort(401)
    errors = {}
    return render_template("report/new.html", errors=errors)


def create():
    if not authenticated(session):
        abort(401)
    """ Se transforma el diccionario inmutable en el que vienen almacenadas las coordenadas
     a un diccionario mutable y se guardan por separados en los campos de longitud y latitud para
     mandarlo al punto nuevo"""
    latLng = json.loads(request.form["coordinates"])
    params = request.form.to_dict()
    del params["coordinates"]

    params["latitude"] = latLng["lat"]
    params["longitude"] = latLng["lng"]
    new_report = Report(**params)
    errors = ReportValidator(new_report).validate_create()
    if errors:
        return render_template("report/new.html", errors=errors, fieldsInfo=new_report)
    db.session.add(new_report)
    db.session.commit()
    return redirect(url_for("reports_index"))


def edit(id):
    if not authenticated(session):
        abort(401)
    report = Report.query.filter(Report.id == id).first()
    errors = {}
    return render_template(
        "report/edit.html", id=report.id, errors=errors, fieldsInfo=report
    )


def editInfo(id):
    if not authenticated(session):
        abort(401)

    latLng = json.loads(request.form["coordinates"])
    params = request.form.to_dict()
    del params["coordinates"]
    params["latitude"] = latLng["lat"]
    params["longitude"] = latLng["lng"]
    new_report = Report(**params)
    report = Report.query.filter(Report.id == id).first()
    errors = ReportValidator(new_report, report).validate_update()

    if errors:
        return render_template(
            "report/edit.html",
            errors=errors,
            id=report.id,
            fieldsInfo=new_report,
        )
    report.title = new_report.title
    report.category = new_report.category
    report.description = new_report.description
    report.latitude = new_report.latitude
    report.longitude = new_report.longitude
    report.state = new_report.state
    report.complainant_telephone = new_report.complainant_telephone
    report.complainant_name = new_report.complainant_name
    report.complainant_last_name = new_report.complainant_last_name
    report.complainant_email = new_report.complainant_email

    db.session.commit()
    return redirect(url_for("reports_index"))


def delete(id):
    if not authenticated(session):
        abort(401)
    report = Report.query.filter(Report.id == id).first()
    db.session.delete(report)
    db.session.commit()
    return redirect(url_for("report_index"))