CREATE TABLE IF NOT EXISTS trainers (
    id SERIAL PRIMARY KEY,
    name TEXT NOT NULL,
    specialization TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS memberships (
    id SERIAL PRIMARY KEY,
    type TEXT NOT NULL,           -- 'time_limited' | 'visit_limited'
    name TEXT NOT NULL,
    start_date DATE,
    end_date DATE,
    visits_left INTEGER
);

CREATE TABLE IF NOT EXISTS clients (
    id SERIAL PRIMARY KEY,
    name TEXT NOT NULL,
    phone TEXT NOT NULL,
    email TEXT NOT NULL,
    membership_id INTEGER REFERENCES memberships(id)
);

CREATE TABLE IF NOT EXISTS trainings (
    id SERIAL PRIMARY KEY,
    name TEXT NOT NULL,
    trainer_id INTEGER NOT NULL REFERENCES trainers(id),
    start_time TIMESTAMP NOT NULL,
    duration_minutes INTEGER NOT NULL,
    capacity INTEGER NOT NULL
);