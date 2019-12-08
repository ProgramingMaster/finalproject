from flask import redirect, session, flash, request
from functools import wraps
import math


# Scale the font size of text based on the length of the text
def scaleSize(text):
    return round(100 / math.log(len(text)*10))

def error(message):
    flash(message, "danger")
    return redirect(request.url)

def success(message):
    flash(message, "primary")
    return redirect(request.url)

# Login Guard
def loginRequired(f):
    """
    Decorate routes to require login.

    http://flask.pocoo.org/docs/1.0/patterns/viewdecorators/
    """
    @wraps(f)
    def decoratedFunction(*args, **kwargs):
        if session.get("userId") is None:
            return redirect("/login")
        return f(*args, **kwargs)
    return decoratedFunction
