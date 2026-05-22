from flask import Blueprint, render_template, request, redirect, session, flash
from db import get_db_connection

log_workout_bp = Blueprint('log_workout', __name__)

@log_workout_bp.route('/log_workout')
def view_log_workout():
    """Visar användarens profil med information från databasen. Kräver inloggning."""
    
    #Skickar användaren till inloggningen om de saknar en aktiv session
    if 'user_id' not in session:
        flash("Du måste logga in för att se din profil.")
        return redirect('/login')

    user_id = session['user_id']
    conn = get_db_connection()
    cursor = conn.cursor()

    sql = "SELECT name, email, weight, height, age FROM peakform.users WHERE user_id = %s"
    cursor.execute(sql, (user_id,))
    user_data = cursor.fetchone()

    cursor.close()
    conn.close()

    return render_template('log_workout.html', logged_in=True, user=user_data)

