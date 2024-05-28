import psycopg2
from config import DB_HOST, DB_USER, DB_PASSWORD, DB_NAME, DB_PORT


def create_connection():
    conn = None
    try:
        conn = psycopg2.connect(
            database = DB_NAME,
            user = DB_USER,
            host = DB_HOST,
            password = DB_PASSWORD,
            port = DB_PORT
        )
        print("Connected to the PostgreSQL database successfully")
        return conn

    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
        return None
    
def error(e):
    print("Wystąpił błąd podczas pobierania danych:", e)
    return {"error": "Wystąpił błąd podczas pobierania danych"}, 500


