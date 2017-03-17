import sqlite3

#from flask_sqlalchemy import SQLAlchemy

from flask import Flask, g, flash, redirect, render_template, request, session, url_for
# from flask_session import Session
from flask_jsglue import JSGlue

#from flask_debugtoolbar import DebugToolbarExtension
#from passlib.apps import custom_app_context as pwd_context
from tempfile import gettempdir

from helpers import *

app = Flask(__name__)

# SQLAlchemy setup
#app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
#app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///builder.db'
#app.config["SQLALCHEMY_ECHO"] = True
#db = SQLAlchemy(app)

JSGlue(app)

#app.debug = True
app.config['SECRET_KEY'] = 'development_key'

# ensure responses aren't cached
if app.config["DEBUG"]:
    @app.after_request
    def after_request(response):
        response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
        response.headers["Expires"] = 0
        response.headers["Pragma"] = "no-cache"
        return response
      
#toolbar = DebugToolbarExtension(app)

#print(app.root_path)

@app.route("/")
def index():
#  logging.warning("See this message in Flask Debug Toolbar!")

  users = query_db('SELECT * FROM users')

  for user in users:
    print('User: ' + user['user_name'])
#    print( user['user_name'] )
   
  themes = query_db('SELECT * FROM themes')
  
  for theme in themes:
    print('Theme: ' + theme['theme_name'])
#    print( theme['theme_name'] )
   
  variables = query_db('SELECT * FROM variables')
  
  for variable in variables:
    varname = variable['var_name']
    message = query_db("SELECT message FROM helptext WHERE var_name = '" + varname + "'")

    print('@' + variable['var_name'] + "=" + variable['output'] + " -- " + message[0]['message'])
#    print(message)
#    query = 'SELECT message FROM helptext WHERE var_name = "' + variable['var_name'] + '"'
#    help = query_db(query)
#    print(help)
#    print( "@" + variable['var_name'] + ": " + variable['output'] + " -- " + help)

  return render_template("index.html")

  


@app.route("/export")
def export():
  return render_template("index.html")
  
  
@app.route("/register")
def register():
  return render_template("index.html")
  
  
@app.route("/login")
def login():
  return render_template("index.html")
  
  
@app.route("/logout")
def logout():
  return render_template("index.html")
  

@app.route("/password")
def password():
  return render_template("index.html")
  
  
@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()

        
        
if __name__ == "__main__":
    app.run()
