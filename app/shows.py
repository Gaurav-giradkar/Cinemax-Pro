import datetime
from flask import Blueprint, render_template, request
from .db import get_db_cursor
from .auth import login_required

bp = Blueprint('shows', __name__, url_prefix='/shows')

@bp.route('/<int:movie_id>')
@login_required
def selection(movie_id):
    date_filter = request.args.get('date')
    if not date_filter:
        date_filter = datetime.date.today().isoformat()

    # ✅ DEFINE dates HERE
    today = datetime.date.today()
    dates = [
        today,
        today + datetime.timedelta(days=1),
        today + datetime.timedelta(days=2)
    ]
        
    cursor = get_db_cursor()
    
    cursor.execute('SELECT * FROM movies WHERE id = %s', (movie_id,))
    movie = cursor.fetchone()
    
    # ✅ NO date filter here (correct)
    query = """
SELECT MIN(s.id) as id, s.time, t.name as theatre_name
FROM shows s
JOIN theatres t ON s.theatre_id = t.id
WHERE s.movie_id = %s
GROUP BY t.name, s.time
ORDER BY t.name, s.time
"""
    cursor.execute(query, (movie_id,))
    shows = cursor.fetchall()
    
    # group by theatre
    grouped_shows = {}
    for show in shows:
        t_name = show['theatre_name']
        if t_name not in grouped_shows:
            grouped_shows[t_name] = []
        grouped_shows[t_name].append(show)
        
    return render_template(
        'shows/selection.html',
        movie=movie,
        shows=grouped_shows,
        selected_date=date_filter,
        dates=dates
    )