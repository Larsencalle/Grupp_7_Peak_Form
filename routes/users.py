from flask import Blueprint, render_template, request, redirect, session, flash
from db import get_db_connection
#from utils import login_required

users_bp = Blueprint('users', __name__)


@users_bp.route('/dashboard')
def dashboard():
    """Visar användarens dashboard och kollar om personen är inloggad."""
    is_logged_in = 'user_id' in session
    return render_template('dashboard.html', logged_in=is_logged_in)


@users_bp.route('/profile')
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


@users_bp.route('/edit_profile')
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


@users_bp.route('/update_profile', methods=['POST'])
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