import psycopg2
from config import DB_HOST, DB_USER, DB_PASSWORD, DB_NAME
from flask import Flask, jsonify, request

app = Flask(__name__)

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


@app.route('/add_route', methods=['POST'])
def add_route_route():
    data = request.json
    id = data.get('Id')
    line_id = data.get('LineId')
    bus_stop_id = data.get('BusStopId')
    order = data.get('Order')

    if not all([id, line_id, bus_stop_id, order]):
        return jsonify({'error': 'Missing parameters'}), 400

    conn = create_connection()
    if conn:
        route_id = add_route(conn, id, line_id, bus_stop_id, order)
        if route_id:
            return jsonify({'route_id': route_id}), 201
        else:
            return jsonify({'error': 'Failed to add route'}), 500
    else:
        return jsonify({'error': 'Database connection failed'}), 500


@app.route('/drivers', methods=['GET'])
def get_routes():
    try:
        connection = create_connection()
        if connection is None:
            return jsonify({"error": "Nie udało się połączyć z bazą danych"}), 500

        cursor = connection.cursor()

        query = "SELECT * FROM public.\"driver\""

        cursor.execute(query)

        routes = cursor.fetchall()

        cursor.close()
        connection.close()

        return jsonify({"drivers": routes})

    except Exception as e:
        print("Wystąpił błąd podczas pobierania danych:", e)
        return jsonify({"error": "Wystąpił błąd podczas pobierania danych"}), 500


if __name__ == '__main__':
    app.run(debug=True)
