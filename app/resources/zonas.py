from flask import redirect, render_template, request, url_for, session, abort
from app.helpers.auth import authenticated
import csv


def index():
    if not authenticated(session):
        abort(401)

    return render_template("zonas/index.html")


def upload_file():
    zone_file = request.files["zone_file"]
    zone_string = zone_file.read().decode("utf-8")

    zone_dict = [
        {k: v for k, v in row.items()}
        for row in csv.DictReader(zone_string.splitlines(), skipinitialspace=True)
    ]

    kk = (
        zone_dict[0]["area"]
        .replace(",", " ")
        .replace("[", " ")
        .replace("]", " ")
        .split()
    )
    import pdb

    pdb.set_trace()

    # with open(kk, newline="") as csvfile:
    #     data = csv.DictReader(csvfile)
    #     print("ID Department Name")
    #     print("---------------------------------")
    #     for row in data:
    #         print(row["name"], row["area"])

    return render_template("zonas/index.html")
