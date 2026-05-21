from flask import Blueprint, render_template, request, redirect, session, flash
from db import get_db_connection
from utils import login_required

auth_bp = Blueprint('auth', __name__)

#INLOGGNING
@auth_bp.route('/login')
def login():
    """Visar inloggningssidan."""
    return render_template('login.html')

@auth_bp.route('/process_login', methods=['POST'])
def process_login():
    """Hanterar inloggningen. Kollar om e-post och lösenord stämmer i databasen."""
    email = request.form.get('email')
    password = request.form.get('password')

    conn = get_db_connection()
    cursor = conn.cursor()

    sql = "SELECT user_id, email FROM peakform.users WHERE email = %s AND password_hash = %s"
    cursor.execute(sql, (email, password))
    
    user = cursor.fetchone()

    cursor.close()
    conn.close()

    if user:
        #Sparar användarens unika ID i sessionen för att hålla personen inloggad överallt
        session['user_id'] = user[0] 
        return redirect('/dashboard')
    else:
        flash("Fel e-post eller lösenord. Försök igen.")
        return redirect('/login')


#SKAPA KONTO
@auth_bp.route('/register')
def register():
    """Visar sidan för att skapa ett nytt konto."""
    return render_template('register.html')

@auth_bp.route('/process_register', methods=['POST'])
def process_register():
    """Sparar en ny användare i databasen om e-posten inte redan finns."""
    name = request.form.get('name')
    email = request.form.get('email')
    password = request.form.get('password')
    
    weight = request.form.get('weight')
    height = request.form.get('height')
    age = request.form.get('age')

    #Omvandlar tomma fält till None så att databasen lagrar de som NULL
    weight = weight if weight else None
    height = height if height else None
    age = age if age else None

    conn = get_db_connection()
    cursor = conn.cursor()

    #Kontrollerar först om e-posten redan används för att förhindra dubletter
    sql_check = "SELECT user_id FROM peakform.users WHERE email = %s"
    cursor.execute(sql_check, (email,))
    existing_user = cursor.fetchone()

    if existing_user:
        cursor.close()
        conn.close()
        flash("E-postadressen är redan registrerad. Vänligen logga in eller välj en annan.")
        return redirect('/register')

    sql_insert = "INSERT INTO peakform.users (name, email, password_hash, weight, height, age) VALUES (%s, %s, %s, %s, %s, %s)"
    cursor.execute(sql_insert, (name, email, password, weight, height, age))
    
    #Commit krävs för att INSERT frågan ska permanent sparas i databasen
    conn.commit()
    cursor.close()
    conn.close()

    return redirect('/login')

@auth_bp.route('/log_out')
def log_out():
    """Loggar ut användaren genom att rensa sessionen."""
    session.pop('user_id', None)
    return redirect('/')