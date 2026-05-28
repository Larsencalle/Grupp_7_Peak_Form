from flask import Blueprint, render_template, request, redirect, session, flash
from db import get_db_connection

exercises_bp = Blueprint('exercises', __name__)

@exercises_bp.route('/exercise')
def exercise():
    """Hämtar alla övningar från databasen och visar övningsdatabase"""
    
    is_logged_in = 'user_id' in session

    conn = get_db_connection()
    if conn is None:
        return "Kunde inte ansluta till databasen.", 500
    cursor = conn.cursor()

    sql = "SELECT exercise_id, name, description, category, difficulty_level, image_url FROM peakform.exercise ORDER BY category DESC"
    cursor.execute(sql)
    exercises_data = cursor.fetchall()

    cursor.close()
    conn.close()

    return render_template('exercise.html', logged_in=is_logged_in, exercises=exercises_data)

@exercises_bp.route('/search', methods=['GET'])
def search():
    """Söker efter övningar baserat på användarens sökord"""
    query = request.args.get('q', '').strip()
    is_logged_in = 'user_id' in session
    
    if not query:
        return redirect('/exercise')
    
    conn = get_db_connection()
    cursor = conn.cursor()
    
    sql = "SELECT exercise_id, name, description, category, difficulty_level, image_url FROM peakform.exercise WHERE name ILIKE %s OR description ILIKE %s ORDER BY name"
    search_term = f"%{query}%"
    cursor.execute(sql, (search_term, search_term))
    results = cursor.fetchall()
    
    cursor.close()
    conn.close()
    
    
    return render_template('exercise.html', logged_in=is_logged_in, exercises=results)

@exercises_bp.route('/exercise/<int:exercise_id>')
def exercise_detail(exercise_id):
    """Visar detaljer om en specifik övning"""
    is_logged_in = 'user_id' in session
    from_page = request.args.get('from', 'exercise') 
    program_id = request.args.get('program_id', None)
    
    conn = get_db_connection()
    if conn is None:
        return "Kunde inte ansluta till databasen.", 500
    cursor = conn.cursor()
    
    sql = "SELECT exercise_id, name, description, category, difficulty_level, image_url FROM peakform.exercise WHERE exercise_id = %s"
    cursor.execute(sql, (exercise_id,))
    exercise = cursor.fetchone()
    
    cursor.close()
    conn.close()
    
    if not exercise:
        flash("Övningen hittades inte.")
        return redirect('/exercise')
    
    
    return render_template('exercise_detail.html', logged_in=is_logged_in, exercise=exercise,  from_page=from_page, program_id=program_id)
