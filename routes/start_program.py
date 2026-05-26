from flask import Blueprint, render_template, request, redirect, session, flash
from db import get_db_connection
#from utils import login_required

start_program_bp = Blueprint('programs', __name__)

@start_program_bp.route('/start_program/<int:program_id>')
def start_program(program_id):
    """ Visar att användaren måste ha ett konto och vara inloggad för att ta del av innehållet"""
    if 'user_id' not in session:
        flash("Du måste logga in för att få tillgång till detta innehåll")
        return redirect('/login')

    user_id = session['user_id']
    conn = get_db_connection()
    cursor = conn.cursor()

  