import sqlite3
from flask import g, redirect, render_template, request, session, url_for
from functools import wraps

DATABASE = 'builder.db'

#
# get_db(): utility class from flask sqlite3 documentation
#
def get_db():
  db = getattr(g, '_database', None)
  if db is None:
      db = g._database = sqlite3.connect(DATABASE)
      
  def make_dicts(cursor, row):
    return dict((cursor.description[idx][0], value)
                for idx, value in enumerate(row))
  
  db.row_factory = make_dicts
#  db.row_factory = sqlite3.Row
  
  
  return db

#
# query_db(): utility class from flask sqlite3 documentation
#
def query_db(query, args=(), one=False):
  cur = get_db().execute(query, args)
  rv = cur.fetchall()
  cur.close()
  
  return (rv[0] if rv else None) if one else rv

#
# query_db(): utility class from flask sqlite3 documentation
#
def insert_db(query, args=()):
  cursor = get_db().cursor()
  result = cursor.execute(query, args)
  get_db().commit()
  
  return result

#
# login_required(): utility class from CS-50 pset
#
def login_required(f):
    """
    Decorate routes to require login.

    http://flask.pocoo.org/docs/0.11/patterns/viewdecorators/
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("user_id") is None:
            return redirect(url_for("login", next=request.url))
        return f(*args, **kwargs)
    return decorated_function
