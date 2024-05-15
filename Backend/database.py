import psycopg2
from config import DB_HOST, DB_USER, DB_PASSWORD, DB_NAME


def create_connection():
    conn = None
    try:
        conn = psycopg2.connect(
            host=DB_HOST,
            user=DB_USER,
            password=DB_PASSWORD,
            dbname=DB_NAME
        )
        print("Connected to the PostgreSQL database successfully")
        return conn

    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
        return None


def add_route(conn, id, line_id, bus_stop_id, order):
    try:
        cur = conn.cursor()
        sql = """
        INSERT INTO public."Route" ("LineId", "BusStopId", "Order")
        VALUES (%s, %s, %s)
        RETURNING "Id"
        """
        cur.execute(sql, (id, line_id, bus_stop_id, order))
        route_id = cur.fetchone()[0]
        conn.commit()
        cur.close()
        return route_id
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
        return None
