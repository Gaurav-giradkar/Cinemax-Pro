from flask import Blueprint, render_template, request
from .db import get_db_cursor
from .auth import login_required

bp = Blueprint('seats', __name__, url_prefix='/seats')

@bp.route('/<int:show_id>')
@login_required
def selection(show_id):
    date = request.args.get('date')

    cursor = get_db_cursor()

    # ✅ show info (NO s.date)
    query = """
    SELECT s.id, s.time, m.title as movie_title, m.poster, t.name as theatre_name
    FROM shows s
    JOIN movies m ON s.movie_id = m.id
    JOIN theatres t ON s.theatre_id = t.id
    WHERE s.id = %s
    """
    cursor.execute(query, (show_id,))
    show_info = cursor.fetchone()

    # ✅ seats
    cursor.execute('SELECT * FROM seats WHERE show_id = %s ORDER BY seat_number', (show_id,))
    seats = cursor.fetchall()

    # ✅ booked seats (DATE BASED)
    cursor.execute("""
SELECT bs.seat_id
FROM booking_seats bs
JOIN bookings b ON bs.booking_id = b.id
WHERE b.show_id = %s AND b.show_date = %s
""", (show_id, date))

    booked = cursor.fetchall()
    booked_seats = [str(row['seat_id']) for row in booked]
    return render_template(
        'seats/selection.html',
        show=show_info,
        seats=seats,
        booked_seats=booked_seats,
        date=date
    )