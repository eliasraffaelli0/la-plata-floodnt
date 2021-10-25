from flask import redirect, render_template, request, url_for, session, abort
from app.helpers.auth import authenticated

def index():
    if not authenticated(session):
        abort(401)

    return render_template("configuracion.html")