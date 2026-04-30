from flask import Flask, render_template, request, redirect, session, flash
from db import get_db_connection

app = Flask(__name__)
app.secret_key = 'nyckel_peakform'


#STARTSIDAN
@app.route('/')
def index():
    return render_template('index.html')


#INLOGGNING
@app.route('/inlogg')
def inlogg():
    return render_template('inlogg.html')

@app.route('/logga_in', methods=['POST'])
def logga_in():
    email = request.form.get('email')
    password = request.form.get('password')

    conn = get_db_connection()
    cursor = conn.cursor()

    sql = "SELECT user_id, email FROM peakform.users WHERE email = %s AND password_hash = %s"
    cursor.execute(sql, (email, password))
    
    anvandare = cursor.fetchone()

    cursor.close()
    conn.close()

    if anvandare:
        session['user_id'] = anvandare[0] 
        return redirect('/dashboard')
    else:
        flash("Fel e-post eller lösenord. Försök igen.")
        return redirect('/inlogg')


#SKAPA KONTO
@app.route('/regkonto')
def regkonto():
    return render_template('regkonto.html')

@app.route('/skapa_konto', methods=['POST'])
def skapa_konto():
    name = request.form.get('name')
    email = request.form.get('email')
    password = request.form.get('password')
    
    weight = request.form.get('weight')
    height = request.form.get('height')
    age = request.form.get('age')

    weight = weight if weight else None
    height = height if height else None
    age = age if age else None

    conn = get_db_connection()
    cursor = conn.cursor()

    sql_check = "SELECT user_id FROM peakform.users WHERE email = %s"
    cursor.execute(sql_check, (email,))
    existerande_anvandare = cursor.fetchone()

    if existerande_anvandare:
        cursor.close()
        conn.close()
        flash("E-postadressen är redan registrerad. Vänligen logga in eller välj en annan.")
        return redirect('/regkonto')

    sql_insert = "INSERT INTO peakform.users (name, email, password_hash, weight, height, age) VALUES (%s, %s, %s, %s, %s, %s)"
    cursor.execute(sql_insert, (name, email, password, weight, height, age))
    
    conn.commit()
    cursor.close()
    conn.close()

    return redirect('/inlogg')


@app.route('/dashboard')
def dashboard():
    inloggad = 'user_id' in session
    return render_template('dashboard.html', logged_in=inloggad)

@app.route('/profil')
def profil():
    if 'user_id' not in session:
        flash("Du måste logga in för att se din profil.")
        return redirect('/inlogg')

    user_id = session['user_id']
    conn = get_db_connection()
    cursor = conn.cursor()

    sql = "SELECT name, email, weight, height, age FROM peakform.users WHERE user_id = %s"
    cursor.execute(sql, (user_id,))
    user_data = cursor.fetchone()

    cursor.close()
    conn.close()

    return render_template('profile.html', logged_in=True, user=user_data)


@app.route('/logga_ut')
def logga_ut():
    session.pop('user_id', None)
    return redirect('/')


if __name__ == '__main__':
    app.run(debug=True)