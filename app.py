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















@app.route('/log_out')
def log_out():
    """Loggar ut användaren genom att rensa sessionen."""
    session.pop('user_id', None)
    return redirect('/')


if __name__ == '__main__':
    app.run(debug=True)