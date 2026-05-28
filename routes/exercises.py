from flask import Blueprint, render_template, request, redirect, session, flash
from db import get_db_connection
from exercise_images import get_exercise_image

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
    
    # Lägg till bildfilnamn för varje övning
    exercises_with_images = []
    for exercise in exercises_data:
        image_url = get_exercise_image(exercise[0])
        exercises_with_images.append((exercise[0], exercise[1], exercise[2], exercise[3], exercise[4], image_url))

    return render_template('exercise.html', exercises=exercises_with_images, logged_in=is_logged_in)

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
    
    # Lägg till bildfilnamn för varje sökresultat
    results_with_images = []
    for result in results:
        image_url = get_exercise_image(result[0])
        results_with_images.append((result[0], result[1], result[2], result[3], result[4], image_url))
    
    return render_template('search_results.html', results=results_with_images, query=query, logged_in=is_logged_in)

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
    
    # Hämta bildfilnamn från exercise_images.py
    image_url = get_exercise_image(exercise[0])
    exercise_with_image = (exercise[0], exercise[1], exercise[2], exercise[3], exercise[4], image_url)
    
    return render_template('exercise_detail.html', exercise=exercise_with_image, logged_in=is_logged_in, from_page=from_page, program_id=program_id)