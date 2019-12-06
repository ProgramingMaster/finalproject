import os

from cs50 import SQL
from flask import Flask, flash, jsonify, redirect, render_template, request, session
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.exceptions import default_exceptions, HTTPException, InternalServerError
from werkzeug.security import check_password_hash, generate_password_hash

from helpers import login_required, scaleSize
import re

# Configure application
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


# Set up local database on development mode. Also configures the SESSION_FILE_DIR
# (which is needed on development mode but messes up production mode)
if os.environ.get('APPLICATION_ENV') == 'dev':
    app.config["SESSION_FILE_DIR"] = mkdtemp()
    db = SQL("sqlite:///finalproject.db")
# Set up stuff in production mode
else:
    # Reroute to https if on http
    # https://stackoverflow.com/questions/32237379/python-flask-redirect-to-https-from-http/50041843
    @app.before_request
    def before_request():
        if request.url.startswith('http://'):
            url = request.url.replace('http://', 'https://', 1)
            code = 301
            return redirect(url, code=code)

    # Set up heroku database
    app.secret_key = 'asdjfklajsfd'
    db = SQL("postgres://zcjxmflvvdjgej:842176674c37fbc83dcc95627716e96dfaf311b1f8b67a50ec52395ee7a5fcbf@ec2-23-21-249-0.compute-1.amazonaws.com:5432/d6dvfncect3bc")

# Configure session to use filesystem (instead of signed cookies)
#app.config["SESSION_FILE_DIR"] = mkdtemp()
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Pipe for scaling the font size of text based on the length of the text
app.jinja_env.filters["scaleSize"] = scaleSize


@app.route("/", methods=["GET", "POST"])
@login_required
def index():
    # Edits weight on a workout if request method is post
    if request.method == "POST":
        # Gets the new weight from the form
        weight = request.form.get("weight")

        # Ensure weight was submitted
        if not weight:
            flash("must provide new weight")
            return redirect("/")

        # Ensure weight is (formatted as) a non negative integer
        if not re.search("\D", weight) == None:
            flash("Weight must be a non negative integer", "danger")
            return redirect('/')

        # Turn weight into an integer
        weight = int(weight)

        # Ensure weight is not an enormous number (the largest deadlift is 1102 lbs)
        if weight > 5000:
            flash("There's no way your lifting that weight", "danger")
            return redirect("/")

        # Grab the workout you want to edit the weight of (this is grabbed from an invisible form whose value is already set to whatever workout your on)
        workout = request.form.get("workout")

        # Ensure workout was submitted
        if not workout:
            flash("must provide new weight", "danger")
            return redirect("/")

        # Query database for workout
        workout = db.execute("SELECT id FROM workouts WHERE userId = :userId AND name = :workout",
                             userId=session["userId"], workout=workout)

        # Ensure the workout exists
        if len(workout) == 0:
            flash("That workout doesn't exist", "danger")
            return redirect("/")

        # Update weight
        db.execute("UPDATE workouts SET weight = :weight WHERE id = :id",
                   weight=weight, id=workout[0]["id"])

        # Show success!
        flash("Edited!", "primary")

        return redirect("/")

    else:
        # Get all of the user's workouts
        workouts = db.execute("SELECT * FROM workouts WHERE userId = :userId", userId=session["userId"])

        return render_template("index.html", workouts=workouts)


@app.route("/create", methods=["GET", "POST"])
@login_required
def create():
    if request.method == "POST":
        # Grab the name of the workout your creating
        name = request.form.get("name")

        # Grab your current weight on the workout, but since this isn't required, set it to zero if not given
        current = request.form.get("current") if request.form.get("current") else "0"

        # Ensure name was submitted
        if not name:
            flash("must provide name of workout", "danger")
            return redirect("/create")

        # Ensure name is not longer then 200 characters
        if len(name) > 200:
            flash("name must not be longer then 200 characters", "danger")
            return redirect("/create")

        # Ensure current is (formatted as) a non negative integer
        if not re.search("\D", current) == None:
            flash("Current weight must be a non negative integer", "danger")
            return redirect('/')

        # Turn weight into an integer
        current = int(current)

        # Ensure current is not an enormous number (the largest deadlift is 1102 lbs)
        if current > 5000:
            flash("There's no way your lifting that weight", "danger")
            return redirect("/create")

        # format name correctly
        name = name.lower().title()

        # Query datbase for workout
        workout = db.execute("SELECT * FROM workouts WHERE userId = :userId AND name = :name",
                             userId=session["userId"], name=name)

        # Ensure the workout doesn't already exist
        if len(workout) > 0:
            flash("that workout already exists", "danger")
            return redirect("/create")

        # Add workout
        db.execute("INSERT INTO workouts (userId, name, weight) VALUES (:userId, :name, :weight)",
                   userId=session["userId"], name=name, weight=int(current))

        # Show success!
        flash("Created!", "primary")

        return redirect("/create")

    else:
        return render_template("create.html")


@app.route("/signup", methods=["GET", "POST"])
def signup():
    if request.method == "POST":
        # Grab username
        username = request.form.get("username")

        # Grab password
        password = request.form.get("password")

        # Grab confirmation password
        confirmation = request.form.get("confirmation")

        # Ensure username was submitted
        if not username:
            flash("must provide username", "danger")
            return redirect("/signup")

        # Ensure password was submitted
        if not password:
            flash("must provide password", "danger")
            return redirect("/signup")

        # Ensure confirmation password was submitted
        if not confirmation:
            flash("must provide confirmation password", "danger")
            return redirect("/signup")

        # Check if username is too long
        if len(username) > 200:
            flash("username is too long", "danger")
            return redirect("/signup")

        # Check if password is too long
        if len(password) > 200:
            flash("password is too long", "danger")
            return redirect("/signup")

        # Ensure password and confirmation password match
        if not confirmation == password:
            flash("password and confimation password don't match", "danger")
            return redirect("/signup")

        # Query database for username
        user = db.execute("SELECT * FROM users WHERE username = :username",
                          username=request.form.get("username"))

        # Check if username already exist
        if len(user) != 0:
            flash("username is not available", "danger")
            return redirect("/signup")

        # Add user
        userId = db.execute("INSERT INTO users (username, hash) VALUES (:username, :passwordHash)",
                            username=username, passwordHash=generate_password_hash(password))

        # Remember user
        session["userId"] = userId

        # Show success!
        flash("Signed up!", "primary")

        return redirect("/")
    else:
        return render_template("signup.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""

    if request.method == "POST":
        username = request.form.get("username")
        # Ensure username was submitted
        if not username:
            flash("must provide username", "danger")
            return redirect("/login")

        # Ensure password was submitted
        elif not request.form.get("password"):
            flash("must provide password", "danger")
            return redirect("/login")

        # Query database for username
        rows = db.execute("SELECT * FROM users WHERE username = :username",
                          username=request.form.get("username"))

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(rows[0]["hash"], request.form.get("password")):
            flash("invalid username and/or password", "danger")
            return redirect("/login")

        # Remember which user has logged in
        session["userId"] = rows[0]["id"]

        # Redirect user to home page
        return redirect("/")

    else:
        return render_template("login.html")


@app.route("/logout")
def logout():
    """Log user out"""

    # Forget any userId
    session.clear()

    # Redirect user to login form
    return redirect("/")


def errorhandler(e):
    """Handle error"""
    if not isinstance(e, HTTPException):
        e = InternalServerError()
    flash(f"{e.name} – {e.code}", "danger")
    return redirect(request.url)


# Listen for errors
for code in default_exceptions:
    app.errorhandler(code)(errorhandler)
