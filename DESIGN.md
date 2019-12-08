#CSLifty
This is a flask app hosted on heroku using a postgres database.__

        ##application.py

    ### Errors & successess
  Instead of using apology, I wrote a new function in helpers.py called error that flashes a message with a
category (the second argument of the flash function) of "danger" and redirects them to wherever they are. The
reason I redirect instead of using render template is because I might be doing more stuff then just rendering the
template if the page was requested via GET (like in index where I'm grabing all of the user's workouts).

  I also use flash for successes (using a category of "primary"), but I didn't make a function for it because I
would only use it three times, and it's looks nicer if you can see that I'm redirecting at the end.


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

  Next is a scaleSize jinja pipe I made. It's used for scaling the font size of text based on the length of the
text. I'll talk about it more later.

    ###Index:
  After that, is the index function. It's GET method gets all of the user's workouts and renders index.html with
the user's workouts as a variable. It's POST method is for editing the weight of the workout. It the grabs the
name of workout you want to change and the weight that you want to change it to.

  After ensuring that both were submitted, it checks if the weight is (formatted as) a non negative integer. It
does this by using regex to look for anything that's not a digit (decimals and negative signs are not digits).
It also ensures the weight isn't larger than 5000 (the world record deadlift weight is 1102).

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

  It then puts current weight through the same validation as the index function put through the edit weight.

  Afterwards, it turns the name to lowercase, then title cases the name, so that it looks good and is consistent
with all the other names. It then ensures that this workout doesn't already exist (also if the names weren't lower
and title cased then squat and SQUAT wouldn't match).

  If everything checks out, I add that workout to the workouts table. The table is structured to have a foreign key
of userId so that I know what users have what workouts.

    ###Signup:
  After that, is the signup function. Its GET method renders signup.html and its POST method signs up a user. After
ensuring that the username, password, and confirmation password were submitted, it ensures that the username and
password aren't too long and that the password and confirmation password match. It also queries the database for the
username to ensure it doesn't already exists (all boiler plate stuff).

    ###Login
  All of this is identical to cs50 finance.

    ###Logout
  Same as finance

    ###errorhandler
  This is the same as finance except instead of using apology I use flash (see the Errors & Sucesses section).

        ##templates

    ###index.html
  The index.html page starts off with a card header that sort of acts like a nav bar with two buttons. I made the
create button have a column width of small so that it will be on the left side of the header, and the logout
button will be on the right side (the two buttons stack on top of eachother on a mobile screen).
  The padding-left 3 (pl-3) on the log out button is so that it's lined up with the create button when on a mobile
  screen (otherwise the logout button would be closer to the left side than the create button would be).

  In the card body there's an accordian where each expandable card in it is a workout that you've made. I used
jinja to loop through all the workouts I gave to index.html in the index function, and make an expandable card
for each workout.

  In the header of the card is the name of the workout and the weight of the workout. There's also
two buttons, and edit button and a create button. I use the col-sm thing again to keep the text on the left side
and the buttons on the right side.

  I also set the font size of the text dynamically, so that long weight names don't take
up so much space. I do this by setting the font size equal to the return value of a jinja pipe I made. This pipe
takes as input my text. I use the ~ operator to concatinize the name of my weight and the weight it self (since
both of them contribute to how long the text is). The ~ operator also makes the weight (which is an integer) a
string. (more on the scaleSize function later)

  The buttons expand the card, but each expands it to reveal a different thing. The edit button expands the edit
section, and the calculate button reveals the calculate section. I gave the edit button a margin left of auto and
the calculate button a margin right of auto of that they would be centered on a mobile screen. I also gave the
edit button a margin right of auto to give the buttons some space from eachother.

  Each card's header has an id, and each of the collapsable sections have id's. Since they're dynamically created,
I use jinja to add the id of the workout to each id, so that they're all unique.

  I'll talk about the edit button first because it's simpler. It just expands the edit section, which is a form
that allows you to change the weight of a workout. There's only one input field here, but I needed a way to let the
server know what workout your actually trying to edit. So I added another input field that already has the name of
the workout as it's value (via jinja). I set it's display to none so that you can't see it.

  Next is the calculate button. This expands the calculate section, but it also does another thing. The button is
also a form, that when submitted calls a javascript function called calWeights that calculates what weights
you need to put on the bar (more on how later). As input it takes the weight of the workout (obviously), but it
also takes the id of the workout. This is because it doesn't just calculates the weights, it also displays them in
the calculate section. It needs the id of the workout to know where to display the weights.

  Inside the calculation section is a row with two h fives and an image in between them. The image is a barbell
and the h fives are where the calWeights function displays what weights to put on the bar. Notice that the
h fives have ids that include the dynamic id of the workout in them. That's you need to input the id of the
workout in the function.

  Below this is a form that lets you calculate the weight of your warmup (which is some percent of your total
weight), along with what weights to put on the bar for that warmup. The input is required and the min and max
attributes are set to 1 and 99 respectivly. The input also has a label on it, I didn't use a placeholder because
the input is too small to have one when you have a max value.

  The form then calls calWarmup which is very similar to calWeights, except it also takes as input what percent
of your total weight you want to use for your warmup. It displays the warmup weight on the h five with the id of
warmupTotal{{ workout.id }}. Below it there's a row that's just like the one above it, it displays what weights
to put on the bar. The bar image is initially has a display of none (all the other h fives are also invisible
since they don't initially have anything in them), but the calWarmup function also sets the barbell display to
inline.

    ###create.html
  This has the same nav bar thing as index.html. It also has a basic form that allows you to create a workout.
The form sends a POST request to /create. Everythings pretty standord, and the name of the workout has a maxLength
of 200. The form also calls a javascript function called disable when submitted. This function disables the submit
button, so that you can't click it twice, which _will_ only make the workout once, but it'll also flash two
messages, one to tell you that you successfully create a workout, and another to tell you that the workout already
exist.

    ###layout.html
  This is just a basic layout. The onlu interesting part is how the flash messages are shown. I use flash
categories to change if the alert is a danger alert or a primary alert.

  First I set the variable messages to be equal to the flashed messages. The "with-categories=true" lets me use
the second argument to a flash function. If messages is not none, then loop through the messages and make an alert
for each message. Each alert shows a message (the first argument to a flash function), and the type of alert is
alert-{{ category }}. For example, if I put "danger" as the second argument to a flash function, the type of
alert would be alert-danger.

  I have a block for the main part of the code in a card with a little padding, and a block for the script right
before the end of the bdoy tag.

    ###login.html
  Basic login stuff, is centered, sends POST request to /login, all inputs are required. I also have a link to the
signup page at the bottom.

    ###signup.html
  Basic signup stuff: is centered, send POST request to /signup, all inputs are required, and the username and
  password have a max length of 200. I also have a link to the login page at the bottom.

      ##helpers.py
  helpers.py has three functions, a scaleSize function, a error function, and a loginRequired function. The
loginRequired function is exactly like the cs50 Finance login_required function, except all the function names a
camelCased because I like that better.

  The scaleSize function is an interesting one. I use it to make long workout names (and weights) in the index
page don't take up so much space. The formula for doing this is complicated, I'm going to disset it for you. I take
the length of the text, multiply it by ten, for the log base 10 of it, divide it into 100, then round it to the
nearest integer. Lets go through why I do all this. I divide it into 100 so that big numbers will return small
numbers and vice versa. I find the log of it so that there all the numbers are close together. The log of 10 is
one, and the log of 100 is two. I multiply it by ten so that it gives bigger numbers, and I do that before finding
the log so that it doesn't make drastic values.

  The error function just flashes a message with the "danger" category. I get the url the user is currently at
with request.url and then I redirct the user there.

      ## calculate.js
  calculate.js has three functions, calWeights, calWarmup and weightsToAdd. The calWeights function displays what
weights to add to the bar for your workout. First it checks to see if no weights are being shown right now by
using the .is(':empty') function in jquery. This is so that you don't calculate the weights everytime you click
the calculate button. It checks both the left and right h fives in case something werid happens and only one side
was added (I don't know what this would be, but I just wanted to be carefull).

  It then calls weightsToAdd, which actually calculates what weights to add to the bar. Then it changes the html
of the h fives on either side of the barbell image to what weightsToAdd returns.

  calWarmup displays what weights to add to the bar for your warmup, along with the weight of the warmup. First
it does some validation, ensuring percent was submitted, is a positive integer (which excludes zero) and is less
than 100. If any of these occur then it just returns, which makes the button do nothing.

  Otherwise, it calculates what weight you should do for your warmup by changing the text of the warmupTotal h
five. Then it calls weightsToAdd with that weight to find what weights to put on the bar for the warmup, and
displays them like calWeights does except on different h fives, along with setting the barbell image's display to
inline (from none).

  Finally comes the weightsToAdd function. This function finds what weights to put on either side of the bar.
After first subtracting the weight of the bar from your weight, it starts at the beginning of the weights array
and simulates adding those weights to both sides of the bar by subtracting those weights from your weight.

  If the total weight is still greater than or equal to zero, then your can add those weights to the bar
(the result arr) without going over your weight. An important note is that you only add one of those
weights to the result arr. This is because the entire result arr will be shown twice (once on each side
of the bar). If your weight is now zero then your done and can return the result arr.

  Otherwise, if your weight is now less than zero, then try a smaller weight (by incrementing i).
If you've tried all the possible weights, then return the result arr like normal but with an extra line
that shows the remainding weight that needs to be added to each side.

  Another important note is that this function doesn't actually return just the result arr. It returns
result array as a string with a br tag between each element (which makes the string vertical).

      ##helpers.js
  This file only has one function, disable, which is only used in create.html to temporaly disable the button when
clicked. Even though it's only used once, it does take a target variable which is the id of the button you want
to disable so that it's re-usable.

      ## finalproject.db
  This is the local databse for the project. The herkoku database is set up the exact same way. It has two tables,
a users table, and a workouts table. The users table is a basic users table with an id column (the primary key),
a username column, and a hash column (which is the hash of the password).

  The workouts table has four coloumns. An id column (the primary key); a userId column (a foreign key), so that
you can know who has the workout; the name of the workout; and the weight of the workout.

  The users table has a unique index on the username column, which is used in login. The workouts table has an
index for the userId, which is used when index gets all the workouts that the usr has. It also has a joint index
(not sure what they're actually called) for the userId and the name of the workout. This index is used alot.
