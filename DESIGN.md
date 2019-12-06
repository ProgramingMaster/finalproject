#CSLifty
This is a flask app hosted on heroku using a postgres database.__

        ##application.py

    ###Configurations:
  Application.py starts off with importing some stuff and doing some basic configurations (boiler plate stuff from
cs50 finance). Then it does some stuff based on if your in development mode (running the site locally via flask run)
or production mode (visiting the site hosted on heroku via going to cslifty.herokuapp.com).

  If your on development mode, then it configures the CS50 Library to use a local SQLite database. Otherwise, it
configures the CS50 Library to use a postgres database on heroku. It also (on production mode) redircts you to
https if your on http.

  Next, wether your on development mode or not, it configures session storage to use filesystem (instead of
signed cookies). This was just something that CS50 Finance did. You may have noticed that if your on development
mode, then it configures SESSION FILE DIR to be equal to mktemp(). This was (again) just something that CS50 Finance
did. But while it's needed when developing locally, it seems to make problems with flash when on production mode.
That's why I made to only happen in development mode.

  Next is a scaleSize jinja pipe I made. It's used for scaling the font size of text based on the length of the text.
I'll talk about it more later.

    ###Index:
  After that, is the index function. It's GET method gets all of the user's workouts and renders index.html with the
user's workouts as a variable. It's POST method is for editing the weight of the workout. It the grabs the name of
workout you want to change and the weight that you want to change it to.

  After ensuring that both were submitted, it checks if the weight is (formatted as) a non negative integer. It does
this by using regex to look for anything that's not a digit (decimals and negative signs are not digits). It also
ensures the weight isn't larger than 5000 (the world record deadlift weight is 1102).

  It checks if workout exists by querying the databse for it. It also uses the id of the workout gotten from
the database to easily find it when updating the weight.

  The input field that holds what weight your trying to edit is actually invisible to you and is inputted for
you. This is because each edit form is specific to that workout anyways, I just needed a way to let the server know
what workout your trying to edit. Of course, a malicious user could still go into the code and change it, which is
why I double check server-side.

    ###Create:
  Next is the create function. Its GET method renders create.html, and its POST method creates a new workout. It
grabs the name of the workout and your current weight on the workout from the form. Since your current weight on
the workout isn't required, it's set to "0" if it's not submitted. Though it does ensure name is submitted.

  It also ensures that name isn't longer than 200 characters (since that feels like a good cut off point).

    ###Signup:
  After that, is the signup function. Its GET method
