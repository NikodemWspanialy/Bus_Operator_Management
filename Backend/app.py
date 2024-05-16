from flask import Flask, jsonify, request
from database import create_connection

app = Flask(__name__)


"""
KIEROWCY
"""


# Wypisywanie kierowców
@app.route('/api/drivers/get', methods=['GET'])
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


# Dodawanie nowego kierowcy.
@app.route('/api/drivers/add', methods=['POST'])
def add_driver():
    try:
        connection = create_connection()
        if connection is None:
            return jsonify({"error": "Nie udało się połączyć z bazą danych"}), 500

        cursor = connection.cursor()

        data = request.json
        name = data.get('name')
        lastname = data.get('lastname')
        license = data.get('license')
        salary = data.get('salary')
        holidays_days = data.get('holidays_days')

        cursor.execute("INSERT INTO driver (name, lastname, license, salary, holidays_days) VALUES "
                       "(%s, %s, %s, %s, %s)", (name, lastname, license, salary, holidays_days))

        connection.commit()

        cursor.close()
        connection.close()

        return jsonify({"message": "Nowy kierowca został dodany pomyślnie"}), 201

    except Exception as e:
        print("Wystąpił błąd podczas dodawania kierowcy:", e)
        return jsonify({"error": "Wystąpił błąd podczas dodawania kierowcy"}), 500


# Usuwanie kierowcy
@app.route('/api/drivers/delete/<int:id>', methods=['DELETE'])
def delete_driver(id):
    try:
        connection = create_connection()
        if connection is None:
            return jsonify({"error": "Nie udało się połączyć z bazą danych"}), 500

        cursor = connection.cursor()

        cursor.execute("DELETE FROM driver WHERE id = %s", (id,))
        connection.commit()

        cursor.close()
        connection.close()

        return jsonify({"message": "Kierowca został usunięty pomyślnie"}), 200

    except Exception as e:
        print("Wystąpił błąd podczas usuwania kierowcy:", e)
        return jsonify({"error": "Wystąpił błąd podczas usuwania kierowcy"}), 500


# Aktualizacja kierowcy
@app.route('/api/drivers/update/<int:id>', methods=['PUT'])
def update_driver(id):
    try:
        if not request.json:
            return jsonify({"error": "Nieprawidłowy format danych JSON"}), 400

        data = request.json
        name = data.get('name')
        lastname = data.get('lastname')
        license = data.get('license')
        salary = data.get('salary')
        holidays_days = data.get('holidays_days')

        if not all([name, lastname, license]):
            return jsonify({"error": "Brak wymaganych pól"}), 400

        connection = create_connection()
        if connection is None:
            return jsonify({"error": "Nie udało się połączyć z bazą danych"}), 500

        cursor = connection.cursor()

        cursor.execute("""
            UPDATE driver
            SET name = %s, lastname = %s, license = %s, salary = %s, holidays_days = %s
            WHERE id = %s
        """, (name, lastname, license, salary, holidays_days, id))
        connection.commit()

        cursor.close()
        connection.close()

        return jsonify({"message": "Dane kierowcy zostały zaktualizowane pomyślnie"}), 200

    except Exception as e:
        print("Wystąpił błąd podczas aktualizowania danych kierowcy:", e)
        return jsonify({"error": "Wystąpił błąd podczas aktualizowania danych kierowcy"}), 500


"""
BUSY
"""


# Wypisywanie busów
@app.route('/api/bus/get', methods=['GET'])
def get_bus():
    try:
        connection = create_connection()
        if connection is None:
            return jsonify({"error": "Nie udało się połączyć z bazą danych"}), 500

        cursor = connection.cursor()

        query = "SELECT * FROM public.\"bus\""

        cursor.execute(query)

        routes = cursor.fetchall()

        cursor.close()
        connection.close()

        return jsonify({"buses": routes})

    except Exception as e:
        print("Wystąpił błąd podczas pobierania danych:", e)
        return jsonify({"error": "Wystąpił błąd podczas pobierania danych"}), 500


# Dodawanie busów
@app.route('/api/bus/add', methods=['POST'])
def add_bus():
    try:
        connection = create_connection()
        if connection is None:
            return jsonify({"error": "Nie udało się połączyć z bazą danych"}), 500

        cursor = connection.cursor()

        data = request.json
        bus_type_id = data.get('bus_type_id')
        next_car_review = data.get('next_car_review')
        actual_event_log_id = data.get('actual_event_log_id')

        cursor.execute("INSERT INTO bus (bus_type_id, next_car_review, actual_event_log_id) VALUES "
                       "(%s, %s, %s)", (bus_type_id, next_car_review, actual_event_log_id))

        connection.commit()

        cursor.close()
        connection.close()

        return jsonify({"message": "Nowy autobus został dodany pomyślnie"}), 201

    except Exception as e:
        print("Wystąpił błąd podczas dodawania autobusu:", e)
        return jsonify({"error": "Wystąpił błąd podczas dodawania autobusu"}), 500


# Usuwanie busów
@app.route('/api/bus/delete/<int:id>', methods=['DELETE'])
def delete_bus(id):
    try:
        connection = create_connection()
        if connection is None:
            return jsonify({"error": "Nie udało się połączyć z bazą danych"}), 500

        cursor = connection.cursor()

        cursor.execute("DELETE FROM bus WHERE id = %s", (id,))
        connection.commit()

        cursor.close()
        connection.close()

        return jsonify({"message": "Autobus został usunięty pomyślnie"}), 200

    except Exception as e:
        print("Wystąpił błąd podczas usuwania autobusu:", e)
        return jsonify({"error": "Wystąpił błąd podczas usuwania autobusu"}), 500


# Aktualizacja busów
@app.route('/api/bus/update/<int:id>', methods=['PUT'])
def update_bus(id):
    try:
        if not request.json:
            return jsonify({"error": "Nieprawidłowy format danych JSON"}), 400

        data = request.json
        bus_type_id = data.get('bus_type_id')
        next_car_review = data.get('next_car_review')
        actual_event_log_id = data.get('actual_event_log_id')

        if not all([bus_type_id, next_car_review]):
            return jsonify({"error": "Brak wymaganych pól"}), 400

        connection = create_connection()
        if connection is None:
            return jsonify({"error": "Nie udało się połączyć z bazą danych"}), 500

        cursor = connection.cursor()

        cursor.execute("""
            UPDATE bus
            SET bus_type_id = %s, next_car_review = %s, actual_event_log_id = %s
            WHERE id = %s
        """, (bus_type_id, next_car_review, actual_event_log_id))
        connection.commit()

        cursor.close()
        connection.close()

        return jsonify({"message": "Dane autobusu zostały zaktualizowane pomyślnie"}), 200

    except Exception as e:
        print("Wystąpił błąd podczas aktualizowania danych autobusu:", e)
        return jsonify({"error": "Wystąpił błąd podczas aktualizowania danych autobusu"}), 500


"""
TRASA AUTOBUSU
"""


# Wypisywanie trasy
@app.route('/api/route/get/<int:line_id>', methods=['GET'])
def get_route(line_id):
    try:
        connection = create_connection()
        if connection is None:
            return jsonify({"error": "Nie udało się połączyć z bazą danych"}), 500

        cursor = connection.cursor()

        query = "SELECT * FROM public.\"route\" WHERE line_id = %s"

        cursor.execute(query, (line_id,))

        routes = cursor.fetchall()

        cursor.close()
        connection.close()

        return jsonify({"routes": routes})

    except Exception as e:
        print("Wystąpił błąd podczas pobierania danych:", e)
        return jsonify({"error": "Wystąpił błąd podczas pobierania danych"}), 500


"""
SPRAWDZENIE PRZYSTANKU
"""


# Wypisanie przytanku
@app.route('/api/trackroute/get/<int:id>', methods=['GET'])
def get_trackroute(id):
    pass


"""
URLOPY
"""


# Wypisywanie urlopów
@app.route('/api/holidays/get', methods=['GET'])
def get_holidays():
    pass


# Dodawanie nowego urlopu
@app.route('/api/holidays/add', methods=['POST'])
def add_holidays():
    pass


# Usuwanie urlopu       NIE WIEM PO CZYM USUWAĆ TO
@app.route('/api/holidays/delete/<int:driver_id>', methods=['DELETE'])
def delete_holidays(driver_id):
    pass


# Aktualizacja urlopu
@app.route('/api/holidays/update/<int:driver_id>', methods=['PUT'])
def update_holidays(driver_id):
    pass


"""
NAPRAWY/PRZEGLĄDY
"""


# Wypisywanie napraw
@app.route('/api/events/get', methods=['GET'])
def get_events():
    pass


# Dodawanie napraw
@app.route('/api/events/add',  methods=['POST'])
def add_events():
    pass


# Usuwanie napraw
@app.route('/api/events/delete/<int:id>', methods=['DELETE'])
def delete_events(id):
    pass


"""
KURSY
"""


# Wypisywanie kursów
@app.route('/api/track/get', methods=['GET'])
def get_track():
    pass


# Dodawanie kursów
@app.route('/api/track/add', methods=['POST'])
def add_track():
    pass


# Usuwanie kursów
@app.route('/api/track/delete/<int:id>', methods=['DELETE'])
def delete_track(id):
    pass


# Aktualizowanie kursów
@app.route('/api/track/update/<int:id>', methods=['PUT'])
def update_track(id):
    pass


"""
SPALANIE --- NIE MA CZEGOŚ TAKIEGO W BAZIE, NIE WIEM CZY WYSZUKUJEMY OGÓLNIE, CZY PO ID
"""


# Wypisywanie spalania
@app.route('/api/combustion)', methods=["GET"])
def get_combustion():
    pass


"""
AWARYJNOŚĆ --- NIE WIEM DO CZEGO TO DAĆ, NIE WIEM CZY WYSZUKUJEMY OGÓLNIE, CZY PO ID
"""


# Wypiswanie awaryjności
@app.route('/api/failure_rate/get', methods=['GET'])
def get_failure_rate():
    pass


"""
RENTOWNOŚĆ LINII - WYSZUKIWANIE OGÓLNE, CZY PO ID
"""


# Wypisywanie rentowności
@app.route('/api/profitability/get', methods=['GET'])
def get_profitability():
    pass


"""
SPALANIE KIEROWCÓW - WYSZUKIWANIE OGÓLNE, CZY PO DRIVERZE
"""


# Wypisywanie spalania
@app.route('/api/driver_combustion/get', methods=['GET'])
def get_driver_combustion():
    pass


if __name__ == '__main__':
    app.run(debug=True)
