from flask import Flask, redirect, url_for, session, current_app as app
from authlib.integrations.flask_client import OAuth


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


def hello_world():
    email = dict(session)["profile"]["email"]
    return f"Hello, you are logge in as {email}!"


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
    resp = google.get("userinfo")  # userinfo contains stuff u specificed in the scrope
    user_info = resp.json()
    user = oauth.google.userinfo()  # uses openid endpoint to fetch user info
    # Here you use the profile/user data that you got and query your database find/register the user
    # and set ur own data in the session not the profile from google
    # session["profile"] = user_info
    session["user"] = user_info["email"]
    session["username"] = user_info["name"]
    import pdb

    pdb.set_trace()
    return redirect("/")
