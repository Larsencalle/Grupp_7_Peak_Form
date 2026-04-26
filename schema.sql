SET search_path TO peakform;


CREATE TABLE users (
    user_id SERIAL PRIMARY KEY,
    email VARCHAR(255) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    age INT,
    weight DECIMAL(5,2),
    height DECIMAL(5,2),
    gender VARCHAR(50)
);


CREATE TABLE exercise (
    exercise_id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    description TEXT,
    category VARCHAR(50),
    difficulty_level INT,
    image_url VARCHAR(255)
);


CREATE TABLE program (
    program_id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    user_id INT REFERENCES users(user_id) ON DELETE CASCADE
);


CREATE TABLE program_exercise (
    program_id INT REFERENCES program(program_id) ON DELETE CASCADE,
    exercise_id INT REFERENCES exercise(exercise_id) ON DELETE CASCADE,
    PRIMARY KEY (program_id, exercise_id)
);


CREATE TABLE workout_session (
    session_id SERIAL PRIMARY KEY,
    user_id INT REFERENCES users(user_id) ON DELETE CASCADE,
    session_date DATE NOT NULL DEFAULT CURRENT_DATE,
    duration_minutes INT
);


CREATE TABLE workout_set (
    set_id SERIAL PRIMARY KEY,
    session_id INT REFERENCES workout_session(session_id) ON DELETE CASCADE,
    exercise_id INT REFERENCES exercise(exercise_id) ON DELETE CASCADE,
    weight DECIMAL(6,2),
    reps INT,
    set_number INT
);