
#CSLifty
  This is a barbell strength training website where you can keep track of your weights, calculate what
weights to put on the bar, and calculate different percentages of your weight (for warmups)

  You can test the app at cslifty.herokuapp.com

  You can test the app locally, on a local database, by running "flask run" on the command line
(while in the final project folder)

  ###__Log in__
  When you open up the page, you will see a basic login form. The username and password can't be empty and if you
  input an incorrect username and password it will show an error. Otherwise it logs you in and brings you to the
  index page.

  There's some text below the form that says, "Don't have an account? Sign up!"

  Clicking signup will bring you to the signup form.

  ###__Sign up__
  The signup form is pretty standard. It will ask you for a username, and a password, along with a confirmation
password which has to match the password. Most the inputs on the site have basic html validators on them (required
and number), but the server double checks everything of course.

  There's also some text below the signup form that says, "Already have an account? Log in!"

  Clicking it will bring you back to the login page.

  ###__Error & Successes__
  Most errors (and successes) throughout the website will be shown with bootstrap alerts. Errors will make a red
alert (along with an error message), and success will make a blue alert (along with an success message). Successes
will only appear when you successfully wrote something to the database (signup, create, edit).

  ###__Index Page__
  When you make an account you will be brought to the index page which contains a bootstrap card and two buttons,
create workout and log out. There're both pretty self explainatory. The create workout button brings you to a form
that allows you to create a workout by inputing the name of the workout and your current weight on the workout.
While the name is required the current weight is not, and will be set to 0 if not inputted. The current weight must
also be a non negative integer not greater than 5000 (because __no one's__ lifting that weight).

  ###__Create Page__
  While on the create page, the button that use to say "create workout" will now say "back to workouts" which
will bring you back to the index page. Once you've created a workout, the index page will have an expandable card
below the buttons showing the name of your workout and what weight your going them at. Creating more workouts will
add more cards.

  ###__Edit__
  Each workout has two buttons to the left of it (or below it if you're on a small screen). The edit button expands
the card to show a form that allows you to edit the weight of the workout. This form has the same restrictions as
the current weight input on the create page.

  ###__Calculate__
  The calculate button also expands the card, but shows something different. It shows a barbell image with a
vertical row of numbers on each side. The numbers represent what weights to put on that side of the barbell
(the numbers will always be the same on both sides as to keep the bar balanced). The weights are conventional
gym weights: 45, 35, 25, 10, 5, and 2.5.

  Sometimes one of the numbers (on each side) will have an R: prefixing it. This stands for remainder, and
means that you have that number left to put on each side, but that number is not a conventional gym weight, which
means you will probably need to round up or down to the nearest weight.

  The calculations will also take into account the 45lb barbell. Which means that if your weight is less than that,
it will just show zeros on each side, since you don't need to put any weights on the bar.

  Strength trainers also warmup before doing there full weight by just doing 50% or 70% of there total weight.
There's a form below the barbell image for just that. You enter what percent of your total weight you want to do
(it must be an integer between 1 and 99 inclusive), and that weight will appear below it. A barbell (just like the
first one) will appear to show what weights to put on the bar to get to that weight.

  The calculation section is what makes this app a *barbell* strength training app. You could still use it to keep
track of any exercises you have that uses weights. But unless your using a 45lb barbell, the calculations won't
work.

  ###__Logout__
  The logout button just logs you out and brings you to the login page.
