from flask import redirect, render_template, request, url_for, session, abort
from app.helpers.auth import authenticated
from app.models.user import User

def index():
    if not authenticated(session):
        abort(401)

    users = User.query.all()
    return render_template("puntos/index.html", users=users)