import sqlite3 as sql

from flask import Flask, g, flash, redirect, render_template, request, session, url_for
from flask_session import Session
from passlib.apps import custom_app_context as pwd_context
from tempfile import gettempdir

#from flask_jsglue import JSGlue

from helpers import *

app = Flask(__name__)

#JSGlue(app)

app.debug = True
app.config['SECRET_KEY'] = 'development_key'

# ensure responses aren't cached
if app.config["DEBUG"]:
    @app.after_request
    def after_request(response):
        response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
        response.headers["Expires"] = 0
        response.headers["Pragma"] = "no-cache"
        return response

#
# @app.route("/") = index(): home (index) page
#

@app.route("/")
@login_required
def index():
  # database query test
  for user in query_db('SELECT * FROM users'):
    print('User: ' + user['user_name'])

  for theme in query_db('SELECT * FROM themes'):
    print('Theme: ' + theme['theme_name'])
  
  for variable in query_db('SELECT * FROM variables'):
    varname = variable['var_name']
    message = query_db("SELECT message FROM helptext WHERE var_name = '" + varname + "'")
    print('@' + variable['var_name'] + "=" + variable['output'] + " -- " + message[0]['message'])

  return render_template("index.html")

#
# @app.route("/register") = register(): new user account creation
#

@app.route("/register", methods=["GET", "POST"])
def register():
  # if user submitted form via POST)
  if request.method == "POST":
    email = request.form.get("email")
    password = request.form.get("password")
    confirmation = request.form.get("confirmation")
    
    # check if email submitted
    if not email:
      flash("must provide email")
      return render_template("register.html")

    # check if password submitted
    elif not password:
      flash("must provide password")
      return render_template("register.html")

    # check if password confirmed and both passwords match
    elif not confirmation or confirmation != password:
      flash("passwords must match")
      return render_template("register.html")
    
    # generate hash based on user's password
    hashed = pwd_context.encrypt(password)
    
    # if user_name is unique, add to db
    exists = query_db('SELECT count(*) AS count FROM users WHERE user_name = ?',(email,))[0]['count']
    
    if not exists:
      result = insert_db(
        'INSERT INTO users (user_name, hash) VALUES (?,?)', (email, hashed)
      )

      if not result:
        flash("can't create user")
        return render_template("register.html")
    else:
      flash("can't create user")
      return render_template("register.html")

    # log user in to application using new account credentials
    login()
    
    # redirect user to home page
    return redirect(url_for("index"))

  # else if user arrived via GET (link or redirect)
  else:
      return render_template("register.html")
    
#
# @app.route("/password") = password(): user can change password
#

@app.route("/password", methods=["GET", "POST"])
@login_required
def password():
  # if user submitted form via POST)
  if request.method == "POST":
    password = request.form.get("password")
    new = request.form.get("new")
    confirmation = request.form.get("confirmation")
    
    # ensure password was submitted
    if not password:
      flash("must provide current password")
      return render_template("password.html")

    # ensure new password was submitted
    elif not new:
      flash("must provide new password")
      return render_template("password.html")

    # ensure password confirmation was submitted and matches new password
    elif not confirmation or confirmation != new:
      flash("passwords must match")
      return render_template("password.html")

    # query database for username
    rows = query_db('SELECT * FROM users WHERE user_id =  ?',(session["user_id"],))

    # ensure username exists and password is correct
    if len(rows) != 1 or not pwd_context.verify(password, rows[0]["hash"]):
      flash("invalid username and/or password")
      return render_template("login.html")
 
    # generate hash based on user's password
    hashed = pwd_context.encrypt(new)

    # update user's password in db
    result = insert_db(
        'UPDATE users SET hash = ? WHERE user_id = ?', (hashed, session["user_id"])
      )
    
    if not result:
      flash("can't update password")
      return render_template("password.html")

    # flash message for flask to update alert message in header on index template
    flash("Password changed!")

    return render_template("password.html")
  
  # else if user arrived via GET (link or redirect)
  else:
    # redirect user to home page
    return render_template("password.html")
  
#
# @app.route("/login") = login(): existing user log in page
#

@app.route("/login", methods=["GET", "POST"])
def login():
  """Log user in."""

  # clear current session user_id
  session.clear()

  # if user submitted form via POST)
  if request.method == "POST":
    email = request.form.get("email")
    password = request.form.get("password")
    confirmation = request.form.get("confirmation")
    
    # check if email submitted
    if not email:
      flash("must provide email")
      return render_template("login.html")

    # check if password submitted
    elif not password:
      flash("must provide password")
      return render_template("login.html")

    # query database for username
    rows = query_db('SELECT * FROM users WHERE user_name =  ?',(email,))

    # ensure username exists and password is correct
    if len(rows) != 1 or not pwd_context.verify(password, rows[0]["hash"]):
      flash("invalid username and/or password")
      return render_template("login.html")
    
    # remember which user has logged in
    session["user_id"] = rows[0]["user_id"]

    # redirect user to home page
    return redirect(url_for("index"))

  # else if user arrived via GET (link or redirect)
  else:
    return render_template("login.html")

#
# @app.route("/logout") = logout(): log user out of application
#

@app.route("/logout")
def logout():
  # clear current session user_id
  session.clear()

  # redirect user to login page
  return redirect(url_for("login"))  

#
# @app.route("/export") = export(): export compiled CSS files
#

@app.route("/export")
def export():
  return render_template("export.html")

#
# close_connection(): utility class from flask sqlite3 documentation
#

@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()

#
# app.run(): main applicatiion function
#

if __name__ == "__main__":
    app.run()
