#
# import python libraries
#

import os
import json
import sqlite3 as sql

from flask import Flask, g, flash, jsonify, redirect, render_template, request, session, url_for
from passlib.apps import custom_app_context as pwd_context
from tempfile import gettempdir

# from flask_jsglue import JSGlue

from helpers import *
#from content import *

#
# instantiate globals
#

app = Flask(__name__)
active_theme = None

#JSGlue(app)

app.debug = True
app.config['SECRET_KEY'] = 'developer key'
#app.config['SECRET_KEY'] = '\x81\xb5\x14\x9a\x1a\xa2\x04\xc3\xc7\xd6\xe3\x98\xd3n\xc0\xe7\xd8\xcej\xba\xef^*\x8a'

#
# ensure responses aren't cached - utility from CS-50 pset
#

if app.config["DEBUG"]:
  @app.after_request
  def after_request(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response
  
#
# init_app(): initialize global variables
#

def init_app(app):
  global active_theme
  active_theme = None
init_app(app)

#
# @app.route("/") = index(): public-facing home page
#

@app.route("/")
def index():
  return render_template("index.html")

#
# @app.route("/theme") = theme(): returns theme layout panel in iframe
#

@app.route("/theme", methods=["GET"])
@login_required
def theme():
  # includes &category=XXX
  category = request.args.get("category")
  return render_template("theme.html", category=category)

#
# @app.route("/login") = login(): user log in page
#

@app.route("/login", methods=["GET", "POST"])
def login():
  # clear current session user_id
  session.clear()

  # if user submitted form via POST
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
    rows = query_db('SELECT * FROM users WHERE name =  ?',(email,))

    # ensure username exists and password is correct
    if len(rows) != 1 or not pwd_context.verify(password, rows[0]["hash"]):
      flash("invalid username and/or password")
      return render_template("login.html")
    
    # remember which user has logged in
    session["user_id"] = rows[0]["id"]

    # redirect user to home page
    return redirect(url_for("user"))

  # else if user arrived via GET (link or redirect)
  else:
    return render_template("login.html")

#
# @app.route("/logout") = logout(): log user out of application
#

@app.route("/logout")
@login_required
def logout():
  global active_theme
  active_theme = None
  # clear current session user_id
  session.clear()

  # redirect user to login page
  return redirect(url_for("index"))  

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
    rows = query_db('SELECT * FROM users WHERE id =  ?',(session["user_id"],))

    # ensure username exists and password is correct
    if len(rows) != 1 or not pwd_context.verify(password, rows[0]["hash"]):
      flash("invalid username and/or password")
      return render_template("login.html")
 
    # generate hash based on user's password
    hashed = pwd_context.encrypt(new)

    # update user's password in db
    result = insert_db(
        'UPDATE users SET hash = ? WHERE id = ?', (hashed, session["user_id"])
      )
    
    if not result:
      flash("can't update password")
      return render_template("password.html")

    # flash message for flask to update alert message in header on index template
    flash("Password changed!")
    return render_template("password.html")
  
  # else if user arrived via GET (link or redirect)
  else:
    return render_template("password.html")
  
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
    
    # if name is unique, add to db
    exists = query_db('SELECT count(*) AS count FROM users WHERE name = ?',(email,))[0]['count']
    
    if not exists:
      result = insert_db('INSERT INTO users (name, hash) VALUES (?,?)', (email, hashed))

      if not result:
        flash("can't create user")
        return render_template("register.html")
    else:
      flash("can't create user")
      return render_template("register.html")

    # log user in to application using new account credentials
    login()
    
    # redirect user to user home page
    return redirect(url_for("user"))

  # else if user arrived via GET (link or redirect)
  else:
      return render_template("register.html")
  
#
# @app.route("/user") = index(): user home page
#

@app.route("/user")
@login_required
def user():
  global active_theme
  
  active_theme = None
  themes = query_db('SELECT * FROM themes WHERE user_id = ?', (session["user_id"],))

  return render_template("user.html", themes=themes)

#
# @app.route("/new") = new_theme(): create new theme in db from default values
#

@app.route("/new", methods=["GET"])
@login_required
def new():
  global active_theme
  active_theme = get_default_theme()
  
  # check to see if this name has been used by current user
  theme_name = request.args.get("n")

  # if name is in use by this user
  if query_db('SELECT * FROM themes WHERE user_id =  ? AND name = ?',(session["user_id"], theme_name)):
    flash("theme name already in use")
    return render_template("user.html")
  # if name is unique and unused
  else:
    # create new theme in themes table
    result = insert_db('INSERT INTO themes (name, user_id) VALUES (?,?)', (theme_name, session["user_id"]))
    
    # validate insert into themes table
    if not result:
      flash("can't create theme")
      return render_template("user.html")
    
    theme_id =  result.lastrowid

    if not theme_id:
      flash("can't create theme")
      return render_template("user.html")

    # clone default theme with new theme id in variables table
    for varObj in active_theme:
      result = insert_db('INSERT INTO variables (name, output, type, category, section, subsection, theme_id) VALUES (?, ?, ?, ?, ?, ?, ?)', (varObj['name'], varObj['output'], varObj['type'], varObj['category'], varObj['section'], varObj['subsection'], theme_id))
      varObj['id'] = result.lastrowid
                  
      # validate insert into variables table
      if not result:
        flash("can't create theme")
        return render_template("user.html")

    # go to first page of theme layout
    return redirect(url_for("category"))

#
# @app.route("/load") = load(): load a theme from the database
#

@app.route("/load", methods=["GET"])
@login_required
def load():
  global active_theme
  theme_id = request.args.get("id")
  active_theme = get_theme(theme_id)
  
  return redirect(url_for("category"))
 
#
# @app.route("/delete") = delete(): delete a theme from the database
#

@app.route("/delete", methods=["GET"])
@login_required
def delete():
  theme_id = request.args.get("id")
  delete_theme(theme_id)
  
  return redirect(url_for("user"))

#
# @app.route("/category") = call after new or load to render category page
#

@app.route("/category", methods=["GET", "POST"])
@login_required
def category():
  global active_theme
  if request.method == "POST":
    post_data = request.form.to_dict()
    post_key = next(iter(post_data))
    post_val = post_data[post_key]
    
    html = get_content(post_val)
  
    return html
  else:
    category = "core"
#    category = request.args.get("c")

    return render_template("application.html", iframe=url_for('theme', category=category), vars=active_theme, messages=get_help_text(), category=category)

#
# @app.route("/save"): save(): 
#

@app.route("/save", methods=["POST"])
@login_required
def save():
  global active_theme
  
  if request.method == "POST":
    result = save_theme(active_theme)
    return json.dumps({'status':'OK'});
  else:
    # redirect user to user home page
    return redirect(url_for("user"))

  
#######################################


#
# @app.route("/update"): update(): 
#

@app.route("/update", methods=["POST"])
@login_required
def update():
  global active_theme
  
  post_data = request.form.to_dict()
  post_key = next(iter(post_data))
  post_val = post_data[post_key]
  
  # DON'T LOOP, JUST FIND MATCH
  
  for var in active_theme:
    if var['name'] == post_key:
      var['output'] = post_val
  
  return json.dumps({'status':'OK'});

#
# @app.route("/getvars"): getvars(): 
#

@app.route("/getvars", methods=["POST"])
@login_required
def getvars():
  global active_theme
  return jsonify(active_theme)

#
# @app.route("/config"): config(): 
#
# NOTE: RENDER TEMPALTE SHOULD BE CALLED WHEN THEME IS FIRST INITIALIZED, INSTEAD OF HAVING
# DUPLICATE HTML IN APPLICATION.HTML AND CONFIGVARS.HTML
#

@app.route("/config", methods=["POST"])
@login_required
def config():
  global active_theme
  
  post_data = request.form.to_dict()
  post_key = next(iter(post_data))
  post_val = post_data[post_key]
  
  rendered = render_template("configvars.html", vars=active_theme, messages=get_help_text(), category=post_val)

  return rendered

#
# @app.route("/export") = export(): export compiled CSS files
#

@app.route("/export", methods=["GET"])
@login_required
def export():
  global active_theme
  return render_template("export.html", vars=active_theme)

#
# tried to have cancel link on change password to act like back()
#

@app.route("/cancel")
def cancel():
  return redirect(redirect_url())





#######################################

#
# user_name(): utility context processor allows get_username to be used in jinja templates
#

@app.context_processor
def utility_processor():
  def user_name():
    # return name of current user in database
    user_name = get_user_name()
    return user_name
  
  # return dict as result of utility_processor call
  return dict(user_name=user_name)

#
# get_layout(): utility context processor allows get_layout to be used in jinja templates
#

# NEXT STEPS: get_content generates html; better if it cleanly read & returned html from text files (easier to process)
# can be loaded once and accessed from memory

@app.context_processor
def utility_processor():
  def get_html(category, vars={}):
    # return html content for a category
    return get_content(category, vars)
  
  # return dict as result of utility_processor call
  return dict(get_html=get_html)

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

  
#
# TECH NOTES
# 
# ADD PARAMETERS TO ROUTE PATH INSTEAD OF PASSING
# see: http://flask.pocoo.org/docs/0.12/quickstart/#rendering-templates
#
# @app.route('/hello/')
# @app.route('/hello/<name>')
# def hello(name=None):
#     return render_template('hello.html', name=name)
#
#
#


