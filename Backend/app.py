from flask import Flask, jsonify, request
from database import create_connection, add_route


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
        id = data.get('id')
        name = data.get('name')
        lastname = data.get('lastname')
        license = data.get('license')
        salary = data.get('salary')
        holidays_days = data.get('holidays_days')

        cursor.execute("INSERT INTO driver (id, name, lastname, license, salary, holidays_days) VALUES "
                       "(%s, %s, %s, %s, %s, %s)", (id, name, lastname, license, salary, holidays_days))

        connection.commit()

        cursor.close()
        connection.close()

        return jsonify({"message": "Nowy kierowca został dodany pomyślnie"}), 201

    except Exception as e:
        print("Wystąpił błąd podczas dodawania kierowcy:", e)
        return jsonify({"error": "Wystąpił błąd podczas dodawania kierowcy"}), 500


# Usuwanie kierowcy
@app.route('api/drivers/delete/<int:driver_id>', methods=['DELETE'])
def delete_driver(driver_id):
    try:
        connection = create_connection()
        if connection is None:
            return jsonify({"error": "Nie udało się połączyć z bazą danych"}), 500

        cursor = connection.cursor()

        cursor.execute("DELETE FROM driver WHERE id = %s", (driver_id,))
        connection.commit()

        cursor.close()
        connection.close()

        return jsonify({"message": "Kierowca został usunięty pomyślnie"}), 200

    except Exception as e:
        print("Wystąpił błąd podczas usuwania kierowcy:", e)
        return jsonify({"error": "Wystąpił błąd podczas usuwania kierowcy"}), 500


# Aktualizacja kierowcy
@app.route('/api/drivers/update/<int:driver_id>', methods=['PUT'])
def update_driver(driver_id):
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
        """, (name, lastname, license, salary, holidays_days, driver_id))
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
    pass


# Dodawanie busów
@app.route('/api/bus/add', methods=['POST'])
def add_bus():
    pass


# Usuwanie busów
@app.route('/api/bus/delete/<int:id>', methods=['DELETE'])
def delete_bus(id):
    pass


# Aktualizacja busów
@app.route('/api/bus/update/<int:id>', methods=['PUT'])
def update_bus(id):
    pass


"""
TRASA AUTOBUSU
"""


# Wypisywanie trasy
@app.route('/api/route/get/<int:line_id>', methods=['GET'])
def get_route(line_id):
    pass


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
def delete_holidays(id):
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
@app.route('/api/profitability/get', mehtods=['GET'])
def get_profitability():
    pass


"""
SPALANIE KIEROWCÓW - WYSZUKIWANIE OGÓLNE, CZY PO DRIVERZE
"""


# Wypisywanie spalania
@app.route('/api/driver_combustion/get', methods=['GET'])
def get_driver_combustion():
    pass