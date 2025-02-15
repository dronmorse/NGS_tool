#!/usr/bin/env python3

from flask import render_template, session, redirect
from functools import wraps

# placeholder render for future sections
def sorry(text, code=400):
    return render_template("sorry.html", text=text, code=code)


def login_required(f):
    """
    Decorate routes to require login.

    https://flask.palletsprojects.com/en/latest/patterns/viewdecorators/
    """

    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("user_id") is None:
            return redirect("/login")
        return f(*args, **kwargs)

    return decorated_function