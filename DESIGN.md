CSLifty
This is a flask app hosted on heroku using a postgres database.

        application.py
_____________________________________________________________________________________________________________________

    Configurations:
  Application.py starts off with importing some stuff and doing some basic configurations (boiler plate stuff from
cs50 finance). Then it does some stuff based on if your in development mode (running the site locally via flask run)
or production mode (visiting the site hosted on heroku via going to cslifty.herokuapp.com).

  If your on development mode, then it configures the CS50 Library to use a local SQLite database. Otherwise, it
configures the CS50 Library to use a postgres database on heroku. It also (on production mode) redircts you to
https if your on http.

  Next, wether your on development mode or not, it configures session storage to use filesystem (instead of
signed cookies). This was just something that CS50 Finance did. You may have noticed that if your on development
mode, then it configures SESSION FILE DIR to be equal to mktemp(). This was (again) just something that CS50 Finance
did. ?But while it's (needed?) when developing locally, it seems to erase the session storage at random when on
production mode.? That's why I made to only happen in development mode.

  Next is a scaleSize jinja pipe I made. It's used for scaling the font size of text based on the length of the text.
I'll talk about it more later.

    Index: there's more to it
  After that, is the index function. It's GET method gets all of the user's workouts and renders index.html with the
user's workouts as a variable. It's POST method is for editing the weight of the workout. It the grabs the name of
workout you want to change and the weight that you want to change it to. It validates the inputs and updates the
weight of the workout.

    Create:
  Next is the create function. Its GET method renders create.html, and its POST method creates a new workout.

    Signup:
  After that, is the signup function. Its GET method
