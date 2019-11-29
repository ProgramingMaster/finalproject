import os

from cs50 import SQL
from flask import Flask, flash, jsonify, redirect, render_template, request, session
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.exceptions import default_exceptions, HTTPException, InternalServerError
from werkzeug.security import check_password_hash, generate_password_hash

from helpers import login_required, flashFormat

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

# Configurations on development mode
if os.environ.get('APPLICATION_ENV') == 'dev':
    app.config["SESSION_FILE_DIR"] = mkdtemp()
    db = SQL("sqlite:///finalproject.db")
# Configurations on production mode
else:
    app.secret_key = 'asdjfklajsfd'
    db = SQL("postgres://zcjxmflvvdjgej:842176674c37fbc83dcc95627716e96dfaf311b1f8b67a50ec52395ee7a5fcbf@ec2-23-21-249-0.compute-1.amazonaws.com:5432/d6dvfncect3bc")

# Configurations either way
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"

Session(app)

app.jinja_env.filters["flashFormat"] = flashFormat

@app.route("/", methods=["GET", "POST"])
@login_required
def index():
    if request.method == "POST":
        weight = request.form.get("weight")

        # Ensure weight was submitted
        if not weight:
            flash("must provide new weight")
            return redirect("/")

        # Check if weight is an integer
        try:
            weight = int(weight)
        except:
            flash("err|current weight must be an integer")
            return redirect("/")

        # Ensure weight was not negative positive
        if weight < 0:
            flash("err|current weight must not be negative")
            return redirect("/")

        workout = request.form.get("workout")

        # Ensure weight was submitted
        if not weight:
            flash("err|must provide new weight")
            return redirect("/")

        # Update weight
        db.execute("UPDATE workouts SET weight = :weight WHERE userId = :userId AND name = :workout", weight=weight, userId=session["userId"], workout=workout)

        flash("suc|Edited!")

        return redirect("/")

    else:
        # Get all of the user's workouts
        workouts = db.execute("SELECT * FROM workouts WHERE userId = :userId", userId=session["userId"])
        return render_template("index.html", workouts=workouts)

@app.route("/create", methods=["GET", "POST"])
@login_required
def create():
    if request.method == "POST":
        name = request.form.get("name")

        # Since current weight isn't required, set it to zero if not given
        current = request.form.get("current") if request.form.get("current") else 0

        # Ensure name was submitted
        if not name:
            flash("err|must provide name of workout")
            return redirect("/create")

        # Ensure current is an integer
        try:
            current = int(current)
        except:
            flash("err|current weight must be an integer")
            return redirect("/create")

        # Ensure current is not negative
        if current < 0:
            flash("err|current weight must not be negative")
            return redirect("/create")

        # format name correctly
        name = name.lower().capitalize()

        # Ensure the workout doesn't already exist
        workout = db.execute("SELECT * FROM workouts WHERE userId = :userId AND name = :name", userId=session["userId"], name=name)

        if len(workout) > 0:
            flash("err|that workout already exists")
            return redirect("/create")

        # Add workout
        db.execute("INSERT INTO workouts (userId, name, weight) VALUES (:userId, :name, :weight)", userId=session["userId"], name=name, weight=int(current))

        flash("suc|Created!")

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
            flash("err|must provide username")
            return redirect("/signup")

        # Ensure password was submitted
        if not password:
            flash("err|must provide password")
            return redirect("/signup")

        # Ensure password and confirmation password match
        if not request.form.get("confirmation") == password:
            flash("err|password and confimation password don't match")
            return redirect("/signup")

        # Check if username already exist
        user = db.execute("SELECT * FROM users WHERE username = :username",
                          username=request.form.get("username"))

        if len(user) != 0:
            flash("err|username is not available")
            return redirect("/signup")

        # Add user
        userId = db.execute("INSERT INTO users (username, hash) VALUES (:username, :passwordHash)",
                    username=username, passwordHash=generate_password_hash(password))

        # Remember user
        session["userId"] = userId

        flash("suc|Signed up!")

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
            flash("err|must provide username")
            return redirect("/login")

        # Ensure password was submitted
        elif not request.form.get("password"):
            flash("err|must provide password")
            return redirect("/login")

        # Query database for username
        rows = db.execute("SELECT * FROM users WHERE username = :username",
                          username=request.form.get("username"))

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(rows[0]["hash"], request.form.get("password")):
            flash("invalid username and/or password")
            return redirect("/login")

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
