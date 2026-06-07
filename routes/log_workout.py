from flask import Blueprint, render_template, request, redirect, session, flash
from db import get_db_connection
from utils import get_workout_history

log_workout_bp = Blueprint('log_workout', __name__)

@log_workout_bp.route('/log_workout')
def view_log_workout():
    """Hämtar och visar användarens kompletta träningshistorik samt antalet pass denna månad."""
    if 'user_id' not in session:
        flash("Du måste logga in.")
        return redirect('/login')

    user_id = session['user_id']
    workout_history = get_workout_history(user_id)

    # Hämtar hur många pass användaren kört denna månad för att visa på sidan
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("""
        SELECT COUNT(*) FROM peakform.workout_session
        WHERE user_id = %s
        AND TO_CHAR(session_date, 'YYYY-MM') = TO_CHAR(NOW(), 'YYYY-MM');
    """, (user_id,))
    antal_pass = cur.fetchone()[0]
    
    cur.close()
    conn.close()

    return render_template(
        'log_workout.html',
        logged_in=True,
        workout_history=workout_history,
        antal_pass=antal_pass
    )