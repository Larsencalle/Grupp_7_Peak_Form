from flask import Flask, render_template, request, redirect, session, flash
from db import get_db_connection

app = Flask(__name__)
app.secret_key = 'nyckel_peakform'


#STARTSIDAN
@app.route('/')
def index():
    """Visar startsidan för PeakForm."""
    return render_template('index.html')


#DASHBOARD
@app.route('/dashboard')
def dashboard():
    """Visar användarens dashboard och kollar om personen är inloggad."""
    is_logged_in = 'user_id' in session
    return render_template('dashboard.html', logged_in=is_logged_in)

@app.route('/profile')
def profile():
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

    return render_template('profile.html', logged_in=True, user=user_data)

@app.route('/exercise')
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

    return render_template('exercise.html', exercises=exercises_data, logged_in=is_logged_in)

@app.route('/search', methods=['GET'])
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
    
    return render_template('search_results.html', results=results, query=query, logged_in=is_logged_in)

@app.route('/exercise/<int:exercise_id>')
def exercise_detail(exercise_id):
    """Visar detaljer om en specifik övning"""
    is_logged_in = 'user_id' in session
    
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
    
    return render_template('exercise_detail.html', exercise=exercise, logged_in=is_logged_in)


@app.route('/edit_profile')
def edit_profile():
    """Visar formuläret för att redigera profiluppgifter."""
    if 'user_id' not in session:
        return redirect('/login')

    user_id = session['user_id']
    conn = get_db_connection()
    cursor = conn.cursor()

    sql = "SELECT name, email, weight, height, age FROM peakform.users WHERE user_id = %s"
    cursor.execute(sql, (user_id,))
    user_data = cursor.fetchone()

    cursor.close()
    conn.close()

    return render_template('edit_profile.html', logged_in=True, user=user_data)


@app.route('/update_profile', methods=['POST'])
def update_profile():
    """Tar emot data från formuläret och uppdaterar databasen."""
    if 'user_id' not in session:
        return redirect('/login')

    user_id = session['user_id']
    
    name = request.form.get('name')
    weight = request.form.get('weight')
    height = request.form.get('height')
    age = request.form.get('age')

    weight = weight if weight else None
    height = height if height else None
    age = age if age else None

    conn = get_db_connection()
    cursor = conn.cursor()

    sql = """
        UPDATE peakform.users 
        SET name = %s, weight = %s, height = %s, age = %s 
        WHERE user_id = %s
    """
    cursor.execute(sql, (name, weight, height, age, user_id))
    

    conn.commit()
    cursor.close()
    conn.close()


    return redirect('/profile')

@app.route('/create_program')
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


@app.route('/save_program', methods=['POST'])
def save_program():
    """Sparar ett nytt träningsprogram och dess kopplade övningar."""
    
    if 'user_id' not in session:
        flash("Grymt program! Skapa ett konto eller logga in för att spara det permanent och börja träna.")
        return redirect('/register')

    user_id = session['user_id']
    program_name = request.form.get('program_name')
    
    selected_exercises = request.form.getlist('selected_exercises') 
    if not selected_exercises:
        flash("Du måste välja minst en övning till ditt program.")
        return redirect('/create_program')

    conn = get_db_connection()
    cursor = conn.cursor()

    sql_program = "INSERT INTO peakform.program (name, user_id) VALUES (%s, %s) RETURNING program_id"
    cursor.execute(sql_program, (program_name, user_id))
    new_program_id = cursor.fetchone()[0]

    sql_exercise = "INSERT INTO peakform.program_exercise (program_id, exercise_id) VALUES (%s, %s)"
    for exercise_id in selected_exercises:
        cursor.execute(sql_exercise, (new_program_id, exercise_id))

    conn.commit()
    cursor.close()
    conn.close()

    flash(f"Ditt program '{program_name}' har sparats!")
    
    return redirect('/my_program')

@app.route('/my_program')
def my_program():
    """Visar en lista över användarens sparade träningsprogram."""
    if 'user_id' not in session:
        flash("Du måste vara inloggad för att se dina program.")
        return redirect('/login')

    user_id = session['user_id']
    conn = get_db_connection()
    if conn is None:
        return "Databasanslutning misslyckades.", 500
        
    cursor = conn.cursor()

    sql = "SELECT program_id, name FROM peakform.program WHERE user_id = %s ORDER BY program_id DESC"
    cursor.execute(sql, (user_id,))
    programs = cursor.fetchall()

    cursor.close()
    conn.close()

    return render_template('my_program.html', logged_in=True, programs=programs)

@app.route('/view_program/<int:program_id>')
def view_program(program_id):
    """Visar alla övningar som tillhör ett specifikt träningsprogram."""
    if 'user_id' not in session:
        return redirect('/login')

    user_id = session['user_id']
    conn = get_db_connection()
    cursor = conn.cursor()

    sql_program = "SELECT name FROM peakform.program WHERE program_id = %s AND user_id = %s"
    cursor.execute(sql_program, (program_id, user_id))
    program = cursor.fetchone()

    if not program:
        flash("Programmet hittades inte eller så har du inte behörighet att se det.")
        return redirect('/my_program')

    sql_exercises = """
        SELECT e.exercise_id, e.name, e.category, e.image_url 
        FROM peakform.program_exercise pe
        JOIN peakform.exercise e ON pe.exercise_id = e.exercise_id
        WHERE pe.program_id = %s
    """
    cursor.execute(sql_exercises, (program_id,))
    exercises = cursor.fetchall()

    cursor.close()
    conn.close()

    return render_template('view_program.html', logged_in=True, program_id=program_id, program_name=program[0], exercises=exercises)

@app.route('/delete_program/<int:program_id>', methods=['POST'])
def delete_program(program_id):
    """Raderar ett helt träningsprogram."""
    if 'user_id' not in session:
        return redirect('/login')

    user_id = session['user_id']
    conn = get_db_connection()
    cursor = conn.cursor()

    sql = "DELETE FROM peakform.program WHERE program_id = %s AND user_id = %s"
    cursor.execute(sql, (program_id, user_id))
    
    conn.commit()
    cursor.close()
    conn.close()

    flash("Programmet har raderats.")
    return redirect('/my_program')


@app.route('/remove_exercise/<int:program_id>/<int:exercise_id>', methods=['POST'])
def remove_exercise(program_id, exercise_id):
    """Tar bort en specifik övning från ett träningsprogram."""
    if 'user_id' not in session:
        return redirect('/login')

    user_id = session['user_id']
    conn = get_db_connection()
    cursor = conn.cursor()

    sql_check = "SELECT 1 FROM peakform.program WHERE program_id = %s AND user_id = %s"
    cursor.execute(sql_check, (program_id, user_id))
    if not cursor.fetchone():
        flash("Du kan inte ändra i detta program.")
        return redirect('/my_program')

    sql_delete = "DELETE FROM peakform.program_exercise WHERE program_id = %s AND exercise_id = %s"
    cursor.execute(sql_delete, (program_id, exercise_id))

    conn.commit()
    cursor.close()
    conn.close()

    flash("Övningen har tagits bort från programmet.")
    
    return redirect(f'/view_program/{program_id}')

if __name__ == '__main__':
    app.run(debug=True)