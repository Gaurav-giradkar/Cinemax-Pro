import mysql.connector
from flask import g

db_config = {
    'host': '127.0.0.1',
    'user': 'root',
    'password': 'root123', # Update to match local environment
    'database': 'cinemax_pro'
}

def get_db():
    if 'db' not in g:
        g.db = mysql.connector.connect(**db_config)
    return g.db

def get_db_cursor(dictionary=True):
    db = get_db()
    return db.cursor(dictionary=dictionary)

def close_db(e=None):
    db = g.pop('db', None)
    if db is not None:
        db.close()

def init_app(app):
    app.teardown_appcontext(close_db)
