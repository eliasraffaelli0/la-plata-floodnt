from flask import redirect, render_template, request, url_for
from app.db import db
from app.models.issue import Issue


# Public resources
def index():
    #conn = connection()
    #issues = Issue.all(conn)

    issues = Issue.query.all()

    
    return render_template("issue/index.html", issues=issues)


def new():
    return render_template("issue/new.html")


def create():
    #conn = connection()
    #Issue.create(conn, request.form)

    new_issue = Issue(**request.form)
    db.session.add(new_issue)
    db.session.commit()

    return redirect(url_for("issue_index"))
