from flask import Flask, render_template, request, redirect, session, flash
from db import get_db_connection

app = Flask(__name__)
app.secret_key = 'nyckel_peakform'


#STARTSIDAN
@app.route('/')
def index():
    """Visar startsidan för PeakForm."""
    return render_template('index.html')


#INLOGGNING
@app.route('/login')
def login():
    """Visar inloggningssidan."""
    return render_template('login.html')

@app.route('/process_login', methods=['POST'])
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
@app.route('/register')
def register():
    """Visar sidan för att skapa ett nytt konto."""
    return render_template('register.html')

@app.route('/process_register', methods=['POST'])
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

@app.route('/edit_profile')
def edit_profile():
    return render_template('edit_profile-html')


@app.route('/log_out')
def log_out():
    """Loggar ut användaren genom att rensa sessionen."""
    session.pop('user_id', None)
    return redirect('/')


if __name__ == '__main__':
    app.run(debug=True)