from flask import jsonify, Blueprint, request, g
from app.models.report import Report
from app.schema.reportSchema import report_schema, report_pagination_schema
from app.validators.reportValidator import ReportValidator
from app.db import db

report_api = Blueprint("reports", __name__, url_prefix="/reports")


@report_api.get("/")
def index():
    # http://127.0.0.1:5000/api/reports/?page=1

    page = int(request.args.get("page", 1))
    # hacer query con un filter imagino?
    report_page = Report.query.paginate(
        page=page, per_page=g.config.elementos_por_pagina
    )

    reports = report_pagination_schema.dump(report_page)

    return jsonify(reports)


@report_api.post("/")
def create():
    new_report = Report(**request.get_json(force=True))
    errors = ReportValidator(new_report).validate_create()
    new_report.state = "unconfirmed"
    if errors:
        response = errors
    else:
        db.session.add(new_report)
        db.session.commit()
        response = report_schema.dump(new_report)
    return jsonify(response)
