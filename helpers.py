import sqlite3
from flask import g, flash, jsonify, redirect, render_template, request, session, url_for
from functools import wraps

DATABASE = 'builder.db'

#
# get_db(): utility from flask sqlite3 documentation
#

def get_db():
  db = getattr(g, '_database', None)
  if db is None:
      db = g._database = sqlite3.connect(DATABASE)
      
  def make_dicts(cursor, row):
    return dict((cursor.description[idx][0], value)
                for idx, value in enumerate(row))
  
  db.row_factory = make_dicts
  # db.row_factory = sqlite3.Row
  
  return db

#
# query_db(): utility from flask sqlite3 documentation
#

def query_db(query, args=(), one=False):
  cur = get_db().execute(query, args)
  rv = cur.fetchall()
  cur.close()
  
  return (rv[0] if rv else None) if one else rv

#
# query_db(): utility from flask sqlite3 documentation
#

def insert_db(query, args=()):
  cursor = get_db().cursor()
  result = cursor.execute(query, args)
  get_db().commit()
  
  return result

#
# login_required(): utility from CS-50 pset
#

def login_required(f):
    # Decorate routes to require login.
    # http://flask.pocoo.org/docs/0.11/patterns/viewdecorators/
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("user_id") is None:
            return redirect(url_for("login", next=request.url))
        return f(*args, **kwargs)
    return decorated_function

#
# default_theme_id(): returns ID of default theme
#

def default_theme_id():
  return query_db('SELECT * FROM themes WHERE name = "default"')[0]['id']

#
# get_default_theme(): returns all vars from default theme
#

def get_default_theme():
  theme = get_theme(default_theme_id())
  
  for var in theme:
    helptext = query_db('SELECT message FROM helptext WHERE var_name = ?',(var['name'],))[0]['message']
    var['message'] = helptext

  return theme

#
# get_theme(): returns all variables for a specified theme
#

def get_theme(themeId):
  data = query_db('SELECT * FROM variables WHERE theme_id = ?',(themeId,))
  
  theme = [ ]
  
  for row in data:
    varObj = { }
    varObj['id'] = row['id']
    varObj['name'] = row['name']
    varObj['output'] = row['output']
    varObj['type'] = row['type']
    varObj['category'] = row['category']
    varObj['section'] = row['section']
    varObj['subsection'] = row['subsection']
    varObj['theme_id'] = row['theme_id']

    theme.append(varObj)
  
  return theme



#
# save_theme( ): returns all variables for a specified theme
#

def save_theme( vars ):
  for var in vars:
    result = insert_db(
        'UPDATE variables SET output = ? WHERE id = ?', (var['output'], var["id"])
      )
  return result





#
# delete_theme(): deletes theme and variables from database
#

def delete_theme(themeId):
  result = insert_db('DELETE FROM themes WHERE id = ?', (themeId,))
  
  if not result:
    flash("can't delete theme")
    return render_template("user.html")
  
  result = insert_db('DELETE FROM variables WHERE theme_id = ?',(themeId,))
  
  if not result:
    flash("can't delete theme")
    return render_template("user.html")

  return result

#
# get_help_text(): returns helper text messages for variables in config ui
#

def get_help_text():
  return query_db('SELECT * FROM helptext')

#
# redirect_url(): utility from flask documentation
#

def redirect_url(default='index'):
#  test = request.args.get('last') or request.referrer or url_for(default)
  test = request.referrer
  print test
  return test

#
# get_user_name(): returns user name based on session user_id 
#

def get_user_name():
  return query_db('SELECT name FROM users WHERE id =  ?',(session["user_id"],))[0]['name']

  
