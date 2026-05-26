from db import get_db_connection

def get_workout_history(user_id):
    conn = get_db_connection()
    cursor = conn.cursor()

    sql = """
        SELECT
            ws.session_id,
            ws.session_date,
            ws.duration_minutes,
            e.name,
            wset.weight,
            wset.reps,
            wset.set_number
        FROM peakform.workout_session ws
        LEFT JOIN peakform.workout_set wset
            ON ws.session_id = wset.session_id
        LEFT JOIN peakform.exercise e
            ON wset.exercise_id = e.exercise_id
        WHERE ws.user_id = %s
        ORDER BY ws.session_date DESC, ws.session_id DESC, wset.set_number ASC
    """

    cursor.execute(sql, (user_id,))
    history = cursor.fetchall()

    cursor.close()
    conn.close()

    return history