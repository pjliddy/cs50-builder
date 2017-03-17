import sqlite3
import execjs
from flask import g, url_for

DATABASE = 'builder.db'

def get_db():
  db = getattr(g, '_database', None)
  if db is None:
      db = g._database = sqlite3.connect(DATABASE)
      
  def make_dicts(cursor, row):
    return dict((cursor.description[idx][0], value)
                for idx, value in enumerate(row))
  
  db.row_factory = sqlite3.Row
  
  return db


def query_db(query, args=(), one=False):
  cur = get_db().execute(query, args)
  rv = cur.fetchall()
  cur.close()
  
  return (rv[0] if rv else None) if one else rv

#def test_less():
#  testfile = url_for('static', filename='/js/test.js')
#  infile = url_for('static', filename='test.less')
#  outfile = url_for('static', filename='test')
#  
#  print(infile)
#  
##  ctx = py_mini_racer.MiniRacer()
#  execjs.eval('node ' + testfile)
#  
##  ctx.eval("var lessTest = () => console.log('test');")
##  ctx.eval("var lessTest = () => var less=require('less');")
#           
##           less.render( input ).then(function(output) {console.log(output.css);};};") 
#
##  ctx.eval("function lessTest(input) { return 5 + 12;};")
#  
##  ctx.call("lessTest")
#
#  return