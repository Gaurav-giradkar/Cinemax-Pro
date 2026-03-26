import uuid
from flask import Blueprint, render_template, request, flash, redirect, url_for, g
from .db import get_db, get_db_cursor
from .auth import login_required

bp = Blueprint('bookings', __name__, url_prefix='/bookings')


@bp.route('/confirm', methods=['POST'])
@login_required
def confirm():
    show_id = request.form.get('show_id')
    date = request.form.get('date')  # ✅ IMPORTANT
    seat_ids = request.form.getlist('seat_ids')

    if not seat_ids:
        flash("Select at least one seat.", "error")
        return redirect(url_for('seats.selection', show_id=show_id, date=date))

    if len(seat_ids) > 10:
        flash("Max 10 seats allowed.", "error")
        return redirect(url_for('seats.selection', show_id=show_id, date=date))

    db = get_db()
    cursor = get_db_cursor()

    try:
        # ✅ CHECK already booked seats (DATE BASED)
        cursor.execute("""
        SELECT bs.seat_id
        FROM booking_seats bs
        JOIN bookings b ON bs.booking_id = b.id
        WHERE b.show_id = %s AND b.show_date = %s
        """, (show_id, date))

        booked = [str(row['seat_id']) for row in cursor.fetchall()]

        for seat in seat_ids:
            if seat in booked:
                db.rollback()
                flash(f"Seat {seat} already booked.", "error")
                return redirect(url_for('seats.selection', show_id=show_id, date=date))

        # ✅ calculate total price
        format_str = ','.join(['%s'] * len(seat_ids))
        cursor.execute(f"SELECT price FROM seats WHERE id IN ({format_str})", tuple(seat_ids))
        prices = cursor.fetchall()
        total_price = sum(float(p['price']) for p in prices)

        # ✅ create booking
        booking_uuid = str(uuid.uuid4())[:8].upper()

        cursor.execute("""
        INSERT INTO bookings (user_id, show_id, show_date, total_price, booking_id)
        VALUES (%s, %s, %s, %s, %s)
        """, (g.user['id'], show_id, date, total_price, booking_uuid))

        booking_id = cursor.lastrowid

        # ✅ insert seats (NO status update)
        for seat_id in seat_ids:
            cursor.execute("""
            INSERT INTO booking_seats (booking_id, seat_id)
            VALUES (%s, %s)
            """, (booking_id, seat_id))

        db.commit()

        return redirect(url_for('bookings.receipt', booking_uuid=booking_uuid))

    except Exception as e:
        db.rollback()
        print("BOOKING ERROR:", e)   # 🔥 IMPORTANT
        flash(str(e), "error")      # show real error
        return redirect(url_for('seats.selection', show_id=show_id))

@bp.route('/receipt/<booking_uuid>')
@login_required
def receipt(booking_uuid):
    cursor = get_db_cursor()

    # ✅ FIXED (NO s.date)
    cursor.execute("""
    SELECT b.*, m.title as movie_title, m.poster,
           t.name as theatre_name, s.time
    FROM bookings b
    JOIN shows s ON b.show_id = s.id
    JOIN movies m ON s.movie_id = m.id
    JOIN theatres t ON s.theatre_id = t.id
    WHERE b.booking_id = %s AND b.user_id = %s
    """, (booking_uuid, g.user['id']))

    booking = cursor.fetchone()

    if not booking:
        flash("Booking not found.", "error")
        return redirect(url_for('movies.index'))

    # seats
    cursor.execute("""
    SELECT s.seat_number
    FROM booking_seats bs
    JOIN seats s ON bs.seat_id = s.id
    WHERE bs.booking_id = %s
    """, (booking['id'],))

    seats = [row['seat_number'] for row in cursor.fetchall()]

    return render_template(
        'bookings/confirmation.html',
        booking=booking,
        seats=seats
    )