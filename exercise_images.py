EXERCISE_IMAGES = {
    1: "benchpress.jpg",                    # Bänkpress
    2: "military_press.jpg",                # Militärpress
    3: "incline_dumbell_press.jpg",         # Lutande Hantelpress
    4: "dips.jpg",                          # Dips
    5: "dumbbell_lateral_raises.jpg",       # Sidolyft med hantlar
    6: "triceps_pushdowns.jpg",             # Triceps Pushdowns
    7: "deadlift.jpg",                      # Marklyft
    8: "pullups.jpg",                       # Pull-ups
    9: "barbell_rowing.jpg",                # Skivstångsrodd
    10: "lat_pull.jpg",                     # Latsdrag
    11: "bicep_curl.jpg",                   # Bicepscurl med hantlar
    12: "squats.jpg",                       # Knäböj (Squats)
    13: "legpress.jpg",                     # Benpress
    14: "lunge_with_dumbells.jpg",          # Utfall med hantlar
    15: "lying_thigh_curl.jpg",             # Liggande Lårcurl
    16: "seated_calf_raise.jpg",            # Sittande Vadpress
}

def get_exercise_image(exercise_id):
    """
    Returnerar bildfilnamnet för en övning baserat på exercise_id.
    """
    return EXERCISE_IMAGES.get(exercise_id)
