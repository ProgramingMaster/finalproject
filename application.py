import os

from cs50 import SQL
from flask import Flask, flash, jsonify, redirect, render_template, request, session
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.exceptions import default_exceptions, HTTPException, InternalServerError
from werkzeug.security import check_password_hash, generate_password_hash

from helpers import login_required

app = Flask(__name__)

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True

# Ensure responses aren't cached
@app.after_request
def after_request(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response

# Configure session to use filesystem (instead of signed cookies)
# app.config["SESSION_FILE_DIR"] = mkdtemp()
app.config["SESSION_PERMANENT"] = False
# app.config["SESSION_TYPE"] = "filesystem"
app.secret_key = 'asdjfklajsfd'
app.config['SESSION_TYPE'] = 'filesystem'
#app.config.from_mapping(
#app.secret_key = 'm3vhIaDWWrAp3QlMwjwk'
#SECRET_KEY = 'm3vhIaDWWrAp3QlMwjwk'
#)
#SESSION_REDIS = redis.from_url(environ.get('SESSION_REDIS'))

Session(app)



db = SQL("postgres://zcjxmflvvdjgej:842176674c37fbc83dcc95627716e96dfaf311b1f8b67a50ec52395ee7a5fcbf@ec2-23-21-249-0.compute-1.amazonaws.com:5432/d6dvfncect3bc")
#db = SQL("sqlite:///finalproject.db")

@app.route("/", methods=["GET", "POST"])
@login_required
def index():
    if request.method == "POST":
        weight = request.form.get("weight")
        if not weight:
            return render_template("index.html", err="must provide new weight")

        try:
            weight = int(weight)
        except:
            return render_template("index.html", err="current weight must be an integer")

        if weight < 1:
            return render_template("index.html", err="current weight must be positive")

        workout = request.form.get("workout")
        if not weight:
            return render_template("index.html", err="must provide new weight")
        db.execute("UPDATE workouts SET weight = :weight WHERE userId = :userId AND name = :workout", weight=weight, userId=session["userId"], workout=workout)
        return redirect("/")

    else:
        workouts = db.execute("SELECT * FROM workouts WHERE userId = :userId", userId=session["userId"])
        return render_template("index.html", workouts=workouts)

@app.route("/create", methods=["GET", "POST"])
@login_required
def create():
    if request.method == "POST":
        name = request.form.get("name")

        current = request.form.get("current") if request.form.get("current") else 0

        # Ensure name was submitted
        if not name:
            return render_template("create.html", err="must provide name of workout")

        try:
            current = int(current)
        except:
            return render_template("create.html", err="current weight must be an integer")

        if current < 1:
            return render_template("create.html", err="current weight must be positive")

        db.execute("INSERT INTO workouts (userId, name, weight) VALUES (:userId, :name, :weight)", userId=session["userId"], name=name, weight=int(current))

        return redirect("/")

    else:
        return render_template("create.html")

@app.route("/signup", methods=["GET", "POST"])
def signup():
    if request.method == "POST":
        username = request.form.get("username")

        password = request.form.get("password")

        # Ensure username was submitted
        if not username:
            return render_template("signup.html", err="must provide username")

        # Ensure password was submitted
        if not password:
            return render_template("signup.html", err="must provide password")

        # Ensure password was submitted
        if not request.form.get("confirmation") == password:
            return render_template("signup.html", err="password and confimation password don't match")

        user = db.execute("SELECT * FROM users WHERE username = :username",
                          username=request.form.get("username"))

        if len(user) != 0:
            return render_template("signup.html", err="username is not available")

        userId = db.execute("INSERT INTO users (username, hash) VALUES (:username, :passwordHash)",
                    username=username, passwordHash=generate_password_hash(password))

        session["userId"] = userId
        return redirect("/")
    else:
        return render_template("signup.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Ensure username was submitted
        if not request.form.get("username"):
            return render_template("login.html", err="must provide username")

        # Ensure password was submitted
        elif not request.form.get("password"):
            return render_template("login.html", err="must provide password")

        # Query database for username
        rows = db.execute("SELECT * FROM users WHERE username = :username",
                          username=request.form.get("username"))

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(rows[0]["hash"], request.form.get("password")):
            return render_template("login.html", err="invalid username and/or password")

        # Remember which user has logged in
        session["userId"] = rows[0]["id"]

        # Redirect user to home page
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")

@app.route("/logout")
def logout():
    """Log user out"""

    # Forget any userId
    session.clear()

    # Redirect user to login form
    return redirect("/")
