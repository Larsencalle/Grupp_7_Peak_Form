from flask import Flask, render_template, request, redirect, session, flash
from db import get_db_connection
from routes.auth import auth_bp
from routes.exercises import exercises_bp
from routes.programs import programs_bp
from routes.users import users_bp
from routes.log_workout import log_workout_bp
#from utils import login_required


app = Flask(__name__)
app.secret_key = 'nyckel_peakform'

app.register_blueprint(auth_bp)
app.register_blueprint(exercises_bp)
app.register_blueprint(programs_bp)
app.register_blueprint(users_bp)
app.register_blueprint(log_workout_bp)

#STARTSIDAN
@app.route('/')
def index():
    """Visar startsidan för PeakForm."""
    return render_template('index.html')


if __name__ == '__main__':
    app.run(debug=True)