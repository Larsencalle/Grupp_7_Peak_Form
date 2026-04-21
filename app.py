from flask import Flask, render_template, request, redirect, session
from db import get_db_connection

app = Flask(__name__)
app.secret_key = 'nyckel_peakform'


# Startsidan 
@app.route('/')
def index():
    return render_template('index.html')

# Inloggningssidan
@app.route('/inlogg')
def inlogg():
    return render_template('inlogg.html')

@app.route('/logga_in', methods=['POST'])
def logga_in():
    email = request.form.get('username')
    losen = request.form.get('password')

    conn = get_db_connection()
    cursor = conn.cursor()

    sql = "SELECT user_id, email FROM peakform.users WHERE email = %s AND password_hash = %s"
    cursor.execute(sql, (email, losen))
    
    anvandare = cursor.fetchone()

    cursor.close()
    conn.close()

    if anvandare:
        session['user_id'] = anvandare[0] 
        print(f"Inloggning lyckades för: {email}")
        return redirect('/dashboard')
    else:
        print("Fel mejl eller lösenord!")
        return redirect('/inlogg')

# Skapa konto-sidan
@app.route('/regkonto')
def regkonto():
    return render_template('regkonto.html')

# Dashboarden
@app.route('/dashboard')
def dashboard():
    inloggad = 'user_id' in session
    
    return render_template('dashboard.html', logged_in=inloggad)

@app.route('/skapa_konto', methods=['POST'])
def skapa_konto():
    email = request.form.get('email')
    losen = request.form.get('losen')

    conn = get_db_connection()
    cursor = conn.cursor()

    sql = "INSERT INTO peakform.users (email, password_hash) VALUES (%s, %s)"
    cursor.execute(sql, (email, losen))
    
    conn.commit()
    cursor.close()
    conn.close()

    return redirect('/inlogg')

@app.route('/logga_ut')
def logga_ut():
    session.pop('user_id', None)
    return redirect('/')


if __name__ == '__main__':
    app.run(debug=True)