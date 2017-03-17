import sqlite3

from flask import Flask, g, flash, redirect, render_template, request, session, url_for
# from flask_session import Session
from flask_jsglue import JSGlue

#from flask_debugtoolbar import DebugToolbarExtension
#from passlib.apps import custom_app_context as pwd_context
from tempfile import gettempdir

from helpers import *

app = Flask(__name__)
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

print(app.root_path)

@app.route("/")
def index():
#  logging.warning("See this message in Flask Debug Toolbar!")

  users = query_db('select * from users')
  
  for user in users:
    print( user['user_name'] )
   
  themes = query_db('select * from themes')
  
  for theme in themes:
    print( theme['theme_name'] )
   
  variables = query_db('select * from variables')
  
  for variable in variables:
    print( variable['name'] )

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
