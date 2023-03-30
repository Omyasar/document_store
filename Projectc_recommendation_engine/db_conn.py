import psycopg2


def db_connection():
    conn = psycopg2.connect(
        host="localhost",
        database="huwebshop",
        user="postgres",
        password="ilijas1",
        port=5432
    )
    cursor = conn.cursor()
    return conn, cursor
