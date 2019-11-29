from flask import redirect, session
from functools import wraps

def flashFormat(message):
    return message[0].split("|")

def login_required(f):
    """
    Decorate routes to require login.

    http://flask.pocoo.org/docs/1.0/patterns/viewdecorators/
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("userId") is None:
            return redirect("/login")
        return f(*args, **kwargs)
    return decorated_function