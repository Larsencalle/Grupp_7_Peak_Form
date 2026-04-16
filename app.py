from flask import Flask, render_template, request, redirect
from db import get_db_connection

app = Flask(__name__)


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

    sql = "SELECT * FROM peakform.users WHERE email = %s AND password_hash = %s"
    cursor.execute(sql, (email, losen))
    
    anvandare = cursor.fetchone()

    cursor.close()
    conn.close()

    if anvandare:
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
    return render_template('dashboard.html')

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

if __name__ == '__main__':
    app.run(debug=True)