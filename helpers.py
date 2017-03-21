import sqlite3
from flask import g, jsonify, redirect, render_template, request, session, url_for
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
# defaultThemeId(): returns ID of default theme
#

def defaultThemeId():
  return query_db('SELECT * FROM themes WHERE name = "default"')[0]['id']

#
# getDefaultTheme(): returns all vars from default theme
#

def getDefaultTheme():
  theme = getTheme(defaultThemeId())
  
  for var in theme:
    helptext = query_db('SELECT message FROM helptext WHERE var_name = ?',(var['name'],))[0]['message']
    var['message'] = helptext

  return theme

#
# getThemeVars(): returns all variables for a specified theme
#

def getTheme(themeId):
  data = query_db('SELECT * FROM variables WHERE theme_id = ?',(themeId,))
  
  theme = [ ]
  
  for row in data:
    varObj = { }
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
# getHelpText(): returns helper text messages for variables in config ui
#

def getHelpText():
  return query_db('SELECT * FROM helptext')

#
# redirect_url(): utility from flask documentation
#

def redirect_url(default='index'):
#  test = request.args.get('last') or request.referrer or url_for(default)
  test = request.referrer
  print test
  return test

