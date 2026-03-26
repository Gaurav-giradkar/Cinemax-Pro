from flask import Blueprint, render_template
from .db import get_db_cursor

bp = Blueprint('movies', __name__)

@bp.route('/')
def index():
    cursor = get_db_cursor()
    cursor.execute('SELECT * FROM movies')
    movies = cursor.fetchall()
    return render_template('movies/index.html', movies=movies)
