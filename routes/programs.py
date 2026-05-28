from flask import Blueprint, render_template, request, redirect, session, flash
from db import get_db_connection
#from utils import login_required

programs_bp = Blueprint('programs', __name__)


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


@programs_bp.route('/save_program', methods=['POST'])
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


@programs_bp.route('/my_program')
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


@programs_bp.route('/view_program/<int:program_id>')
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

    sql_available_exercises = """
        SELECT exercise_id, name, category
        FROM peakform.exercise
        WHERE exercise_id NOT IN (
            SELECT exercise_id
            FROM peakform.program_exercise
            WHERE program_id = %s
        )
        ORDER BY category, name
    """
    cursor.execute(sql_available_exercises, (program_id,))
    available_exercises = cursor.fetchall()

    cursor.close()
    conn.close()

    return render_template(
        'view_program.html', 
        logged_in=True, 
        program_id=program_id, 
        program_name=program[0], 
        exercises=exercises,
        available_exercises=available_exercises
    )


@programs_bp.route('/delete_program/<int:program_id>', methods=['POST'])
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


@programs_bp.route('/remove_exercise/<int:program_id>/<int:exercise_id>', methods=['POST'])
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

@programs_bp.route('/add_exercise/<int:program_id>', methods=['POST'])
def add_exercise(program_id):
    
    if 'user_id' not in session:
        return redirect('/login')
    
    user_id = session['user_id']
    exercise_ids = request.form.getlist('exercise_ids')
    
    if not exercise_ids:
        flash("Välj övning")
        return redirect(f'/view_program/{program_id}')
    
    conn = get_db_connection()
    cursor = conn.cursor()

    sql_check = """
        SELECT 1
        FROM peakform.program 
        WHERE program_id = %s AND user_id = %s
    """
    cursor.execute(sql_check, (program_id, user_id))
    
    if not cursor.fetchone():
        cursor.close()
        conn.close()
        flash("Du kan inte ändra i detta program")
        return redirect('/my_program')
    
    sql_insert = """
        INSERT INTO peakform.program_exercise (program_id, exercise_id)
        VALUES (%s, %s)
    """

    for exercise_id in exercise_ids:
        cursor.execute(sql_insert, (program_id, exercise_id))
    
        
    conn.commit()
    cursor.close()
    conn.close()

    flash("Övningen har lagts till i programmet.!")
    return redirect(f'/view_program/{program_id}')

@programs_bp.route('/start_program/<int:program_id>')
def start_program(program_id):
    """Visar det valda programmets innehåll med navigeringsstöd"""
    if 'user_id' not in session:
        flash("Du måste logga in för att få tillgång till detta innehåll")
        return redirect('/login')

    user_id = session['user_id']
    conn = get_db_connection()
    cursor = conn.cursor()
    

    sql_program = "SELECT name FROM peakform.program WHERE program_id = %s AND user_id = %s"
    cursor.execute(sql_program, (program_id, user_id))
    program = cursor.fetchone()

    if not program:
        cursor.close()
        conn.close()
        flash("Programmet hittades inte.")
        return redirect('/my_program')

   
    sql_exercises = """
        SELECT e.exercise_id, e.name, e.description, e.category, e.difficulty_level, e.image_url 
        FROM peakform.program_exercise pe
        JOIN peakform.exercise e ON pe.exercise_id = e.exercise_id
        WHERE pe.program_id = %s
    """
    cursor.execute(sql_exercises, (program_id,))
    exercises = cursor.fetchall()
    
    cursor.close()
    conn.close()

   
    selected_id = request.args.get('exercise_id', type=int)
    
    current_index = 0
    if exercises:
        if selected_id:
            active_exercise = next((e for e in exercises if e[0] == selected_id), exercises[0])
        else:
            active_exercise = exercises[0]
            
 
        current_index = next((i for i, e in enumerate(exercises) if e[0] == active_exercise[0]), 0)
    else:
        active_exercise = None

    return render_template(
        'start_program.html', 
        logged_in=True, 
        program_id=program_id, 
        program_name=program[0], 
        exercises=exercises,
        active_exercise=active_exercise,
        current_index=current_index,
        total_exercises=len(exercises)
    )