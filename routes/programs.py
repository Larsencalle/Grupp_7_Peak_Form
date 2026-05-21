from flask import Blueprint, render_template, request, redirect, session, flash
from db import get_db_connection
from utils import login_required




@programs_bp.route('/create_program')
def create_program():
    """Visar sidan där man bygger ett program. Fungerar både för inloggade och utloggade."""
    is_logged_in = 'user_id' in session
    
    conn = get_db_connection()
    cursor = conn.cursor()
    

    sql = "SELECT exercise_id, name, category FROM peakform.exercise ORDER BY category, name"
    cursor.execute(sql)
    all_exercises = cursor.fetchall()
    
    cursor.close()
    conn.close()

    return render_template('create_program.html', logged_in=is_logged_in, exercises=all_exercises)