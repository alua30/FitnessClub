import psycopg


DB_DSN = "dbname=fitness_club user=fitness_user password=fitness123 host=localhost port=5432"


def get_connection():
    return psycopg.connect(DB_DSN)