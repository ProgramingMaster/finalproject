#CSLifty
This is a flask app hosted on Heroku using a Postgres database.

        ##application.py


    ###Configurations:
  Application.py starts off with importing some stuff (including helper functions from helper.py) and doing some
basic configurations from cs50 Finance. Then it does some stuff based on if your in development mode (running the
site locally via flask run) or production mode (visiting the site hosted on Heroku via going to
cslifty.herokuapp.com).

  If you're on development mode, then it configures the CS50 Library to use a local SQLite database. Otherwise, it
configures the CS50 Library to use a Postgres database on Heroku, along with adding secret key (which is needed on
Heroku. It also (on production mode) redirects you to https if you're on http. It does this by first checking if the
url starts with http, and if so, it redirects you to the same url, but with the http replaced with https.

  Next, whether your on development mode or not, it configures session storage to use filesystem (instead of
signed cookies). You may have noticed that if you're on development mode, then it configures SESSION FILE DIR to be
equal to mktemp(). This configuration _is_ needed when developing locally, but it makes problems with flash when
on production mode. That's why I made to only happen in development mode.

  Next is a scaleSize jinja pipe I made. It's used for scaling the font size of text based on the length of the
text. I'll talk about how it works later.

    ###Index:
  After that, is the index function. Its GET method gets all of the user's workouts (ordered alphabetically and
renders index.html with the user's workouts as a variable. Its POST method is for editing the weight of the
workout. It grabs the name of the workout you want to change and the weight that you want to change it to.

  After ensuring that both were submitted, it checks if the weight is (formatted as) a nonnegative integer. It
does this by using regex to look for anything that's not a digit. This also checks if the weight is negative
or a decimal number since decimals and negative signs are not digits.

  Then it ensures the weight isn't larger than 1200 (the world record deadlift weight is 1102).

  After that, it ensures the workout exists by querying the database for it. It also grabs the id of the workout
gotten from the database to use later when updating the weight.

  The input field that holds what weight you're trying to edit is actually invisible to you and is inputted for
you. This is because each edit form is specific to that workout anyways; I just needed a way to let the server know
what workout you're trying to edit. Of course, a malicious user could still go into the code and change it, which is
why I double-check server-side.

  Finally, it looks for what workout to change by searching for its id (grabbed earlier) and changes it's weight
column to the new weight you inputted.

    ### Errors & successes
  Instead of using apology, I wrote a new function in helpers.py called error that flashes a message with a
category of "danger" and redirects them to wherever they currently are. Categories are the second argument of a
flash function. The reason I redirect instead of using render template is because I might be doing more stuff then
just rendering the template if the page was requested via GET (like in index where I'm grabbing all of the user's
workouts).

  I also use flash for successes (using a category of "primary"), but I didn't make a function for it because I
would only use it three times, and I think the code is easier to understand how it is. You can see that I'm
redirecting you instead of seeing a mysterious function.

    ###Create:
  Next is the create function. Its GET method renders create.html, and its POST method creates a new workout. It
grabs the name of the workout and your current weight on the workout from the form. Since your current weight on
the workout isn't required, it's set to "0" if it's not submitted. Though it does ensure name is submitted.

  It then ensures that the current weight is a nonnegative integer in the same way that the index function did.

  Then, it converts the name to lowercase, and then title case, so that it looks good and is consistent
with all the other names. SQUAT and squat both become Squat. This also makes it easier to check if the workout
already exists, which it does right after.

  If everything checks out, it adds that workout to the workouts table. The table is structured to have a foreign
key of userId so that It can know what users have what workouts.

    ###Signup:
  After that, is the signup function. Its GET method renders signup.html, and its POST method signs up a user. After
ensuring that the username, password, and confirmation password were submitted, it ensures the password and
confirmation password match. It also queries the database for the username to ensure it doesn't already exist.

    ###Login
  All of this is identical to cs50 finance.

    ###Logout
  Same as finance

    ###errorhandler
  This is the same as finance, except instead of using apology I use flash (see the Errors & Successes section).

        ##templates

    ###index.html
  The index.html page starts off with a card header with a create workout button and a logout button. I made the
create button have a column width of small, and the logout button has a column width of extra small (which means
it only takes up as much space as it needs). This makes it so that the create button will be on the left side
of the header, and the logout button will be on the right side (the two buttons stack on top of each other on a
mobile screen).

  The padding-left 3 (pl-3) on the log out button is so that it's lined up with the create button when on a mobile
  screen.

  In the card body there's an accordion where each expandable card in it is a workout that you've made. I used
jinja to loop through all the workouts I gave to index.html in the index function, and make an expandable card
for each workout.

  In the header of the card is the name of the workout and the weight of the workout. There's also
two buttons, an edit button, and a create button. I used the col-sm thing again to keep the text on the left side
and the buttons on the right side.

  I also set the font size of the text dynamically, so that long weight names don't take up so much space. I do
this by setting the font size equal to the return value of a jinja pipe called scaleSize that I made. I used
the ~ operator to concatenate the name of the workout and the weight of the workout, and fed it to the pipe (since
both of them contribute to how long the text is). The ~ operator also makes the weight (which is an integer) a
string.

  The buttons expand the card, but each expands it to reveal a different thing. The edit button expands the edit
section, and the calculate button expands the calculate section. I gave the edit button a margin left of auto and
the calculate button a margin right of auto so that they would be centered on a mobile screen. I also gave the
edit button a margin right of one to give the buttons some space from each other.

  Each card's header has an id, and each of the collapsible sections have id's. Since they're dynamically created,
I used jinja to add the id of the workout to each id, so that they're all unique.

  I'll talk about the edit button first because it's simpler. It just expands the edit section, which is a form
that allows you to change the weight of a workout. There's only one input field here, but I needed a way to let the
server know what workout you're actually trying to edit. So I added another input field that already has the name of
the workout as its value (via jinja). I set its display to none so that you can't see it (I used display none
instead of visibility hidden so that it also doesn't take up any space.

  Next is the calculate button. This expands the calculate section, but it also does another thing. The button is
also a form, that when submitted, it calls a javascript function called calWeights that calculates what weights
you need to put on the bar (more on how later). As input it takes the weight of the workout (obviously), but it
also takes the id of the workout. This is because it doesn't just calculates the weights: it also displays them in
the calculate section. It needs the id of the workout to know where to display the weights (since the cards are
created dynamically).

  Inside the calculation section is a row with two h fives and an image in between them. The image is a barbell
and the h fives are where the calWeights function displays what weights to put on the bar. Notice that the
h fives have ids that include the dynamic id of the workout in them. That's you need to input the id of the
workout in the function.

  Below this is a form that lets you calculate the weight of your warmup (which is some percent of your total
weight), along with what weights to put on the bar for that warmup. The input is required and the min and max
attributes are set to 1 and 99 respectively. The input also has a label on it, I didn't use a placeholder because
the input is too small to have one when you have a max value.

  The form then calls calWarmup, which is very similar to calWeights, except it also takes as input what percent
of your total weight you want to use for your warmup. It displays the warmup weight on the h five with the id of
warmupTotal{{ workout.id }}. Below it there's a row that's just like the one above it. It displays what weights
to put on the bar. The bar image initially has a display of none, but the calWarmup function also sets the
barbell's display to inline. All the other h fives don't initially have anything in them, which makes them
invisible as well. They do take up space, though, since I wanted spacing on the bottom anyways.

    ###create.html
  This has the same header with two buttons as index.html. It also has a basic form that allows you to create a
workout. The form sends a POST request to /create. Everything's pretty standard. The form also calls a javascript
function called disable when submitted. This function disables the submit button, so that you can't accidentally
click it twice, which _will_ only make the workout once, but it'll also flash two messages, one to tell you that
you successfully create a workout, and another to tell you that the workout already exist (since you just created
it).

    ###layout.html
  This is just a basic layout. The only interesting part is how the flash messages are shown. I used flash
categories to change if the alert is a danger alert or a primary alert.

  First I set the variable messages to be equal to the flashed messages. The "with-categories=true" lets me use
the second argument of a flash function. If messages is not none, then loop through the messages and make an alert
for each message. Each alert shows a message (the first argument to a flash function), and the type of alert is
alert-{{ category }}. If I put "danger" as the second argument to a flash function, the type of alert would be
alert-danger.

  I have a block for the main part of the code in a card with a little padding, and a block for the script outside
of it.

    ###login.html
  Basic login stuff. It's centered, it sends a POST request to /login, all inputs are required. I also have a link
to the signup page at the bottom.

    ###signup.html
  Basic signup stuff. It's centered, it sends a POST request to /signup, all inputs are required. I also have a
link to the login page at the bottom.

      ##helpers.py
  helpers.py has three functions, a scaleSize function, an error function, and a loginRequired function. The
loginRequired function is exactly like the cs50 Finance login_required function, except all the function names are
camelCased because I like that better.

  The scaleSize function is an interesting one. I use it to make long workout names (and their weights) in the index
page not take up so much space. The formula for doing this is complicated, so I'm going to dissect it for you. I take
the length of the text, multiply it by ten, find the log base 10 of it, divide 100 by it, then round it to the
nearest integer. Lets go through why I do all this. I divide it into 100 so that big numbers will return small
numbers and vice versa. I find the log of it so that there all the numbers are close together. The log of 10 is
one, and the log of 100 is two. I multiply it by ten so that it gives bigger numbers, and I do that before finding
the log so that it doesn't make drastic values.

  The error function just flashes a message with the "danger" category. I get the url the user is currently at
with request.url and then I redirect the user there.

      ## calculate.js
  calculate.js has three functions, calWeights, calWarmup and weightsToAdd. The calWeights function displays what
weights to add to the bar for your workout. First it checks to see if no weights are being shown right now by
using the .is(':empty') function in jquery. This is so that you don't calculate the weights everytime you click
the calculate button. It checks both the left and right h fives in case something werid happens and only one side
was added (I don't how this would happen, I just wanted to be carefull).

  It then calls weightsToAdd, which actually calculates what weights to add to the bar. Then it changes the html
of the h fives on either side of the barbell image to what weightsToAdd returns. The weightsToAdd function
returns a string with br tags in it. That's why it changes the html and not the text.

  The calWarmup function displays what weights to add to the bar for your warmup, along with the weight of the
warmup. First it does some validation, ensuring percent was submitted, is a positive integer (which excludes zero)
and is less than 100. If any of these occur then it just returns, which makes the button do nothing.

  Otherwise, it calculates [percent] percent of your total weight (which is your warmup weight) and changes the
text of the warmupTotal h five to that. Then it calls weightsToAdd with the warmup weight to find what weights to
put on the bar for the warmup, and displays them like calWeights does except on different h fives, along with
setting the barbell image's display to inline (from none).

  Finally comes the weightsToAdd function. This function finds what weights to put on either side of the bar.
First it subtracts the weight of the bar from your weight, and if your weight if now zero or less, then it just
returns 0 because you don't need to put any weights on the bar.

  Then it starts at the beginning of the weights array and simulates adding those weights to both sides of the
bar by trying to subtract that weight multiplied by two from your weight. You multiply the weight by two before
subtracting it from your weight because your trying to add it to both sides of the bar.

  If you can do this without making your weight negative, then do it for real (subtract the weight multiplied by
two). Then add the weight (not multiplied by two) to the result array. The reason that you don't first multiply
the weight by two is that entire result arr will be shown twice (once on each side of the bar).

  If the weight is now zero then the while loop will stop the function will carry on to return the result arr.

  Otherwise, if your weight is now less than zero, then try a smaller weight by incrementing i and starting over.
If you've tried all the possible weights, then return the result arr like normal but with an extra line
that shows the remaining weight that needs to be added to each side.

  Another important note is that this function doesn't actually return just the result arr. It returns
result array as a string with a br tag between each element (which makes the string vertical).

      ##helpers.js
  This file only has one function, disable, which is only used in create.html to temporarily disable the button when
clicked. Even though it's only used once, it does take a target variable as input which is the id of the butto
you want to disable so that it's re-usable.

      ## finalproject.db
  This is the local databse for the project. The herkoku database is set up the exact same way. It has two tables,
a users table, and a workouts table. The users table is a basic users table with an id column (the primary key),
a username column, and a hash column (which is the hash of the password).

  The workouts table has four colomns. An id column, which is the primary key. A userId column (a foreign key),
that is used to know who has the workout. Finally, there is a column for the name of the workout, and a column for
the weight of the workout.

  The users table has a unique index on the username column, which is used in the login function (in
application.py).

  The workouts table has an index for the userId, which is used when the index function (in application.py)
gets all the workouts that the user has. It also has a joint index (not sure what they're actually called) for
the userId and the name of the workout. This index is used alot because workout names are only unique to the user.
If you want to find the weight of a workout, you have to not only search that has the same name as the one your
looking for, and the same userId as the one that's logged in
