from flask import redirect, url_for, flash, session, current_app as app
from authlib.integrations.flask_client import OAuth
from app.models.user import User
from app.db import db


# oAuth Setup
oauth = OAuth(app)
google = oauth.register(
    name="google",
    client_id="141121851737-h5o9d32qge3rsnfh8ersp0e7opf20b86.apps.googleusercontent.com",
    client_secret="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",
    access_token_url="https://accounts.google.com/o/oauth2/token",
    access_token_params=None,
    authorize_url="https://accounts.google.com/o/oauth2/auth",
    authorize_params=None,
    api_base_url="https://www.googleapis.com/oauth2/v1/",
    userinfo_endpoint="https://openidconnect.googleapis.com/v1/userinfo",  # This is only needed if using openId to fetch user info
    client_kwargs={"scope": "openid email profile"},
)


def login():
    google = oauth.create_client("google")  # create the google oauth client
    redirect_uri = url_for("authorize", _external=True)
    return google.authorize_redirect(redirect_uri)


# @app.route("/authorize")
def authorize():
    google = oauth.create_client("google")  # create the google oauth client
    token = (
        google.authorize_access_token()
    )  # Access token from google (needed to get user info)
    resp = google.get("userinfo")  # userinfo contains stuff u specificed in the scope
    user_info = resp.json()
    user = User.query.filter(User.email == user_info["email"]).first()
    if user:
        if user.activo:
            session["user"] = user_info["email"]
            session["username"] = user_info["name"]
            session["userId"] = user.id
            return redirect(url_for("home"))
        else:
            flash("Clave incorrecta o usuario inactivo")
            return redirect(url_for("home"))
    else:
        new_user = User()
        new_user.first_name = user_info["given_name"]
        new_user.last_name = user_info["family_name"]
        new_user.username = user_info["name"]
        new_user.email = user_info["email"]
        new_user.activo = 0
        db.session.add(new_user)
        db.session.commit()
        return redirect(url_for("home"))
