from flask import Blueprint, render_template, request, redirect, session, flash
from db import get_db_connection
from utils import get_workout_history

log_workout_bp = Blueprint('log_workout', __name__)

@log_workout_bp.route('/log_workout')
def view_log_workout():
    if 'user_id' not in session:
        flash("Du måste logga in.")
        return redirect('/login')

    user_id = session['user_id']
    workout_history = get_workout_history(user_id)

    return render_template(
        'log_workout.html',
        logged_in=True,
        workout_history=workout_history
    )
