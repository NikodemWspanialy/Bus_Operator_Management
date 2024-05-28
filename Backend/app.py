from flask import Flask, jsonify, request
from flask_restx import Api, Resource, fields
from database import create_connection, error
from Queries.driverDB import driverGetAll, driverCreate, driverGetById, driverDelete, driverUpdate
from Queries.BusDB import busGetAll, busCreate, busDelete, busGetById, busUpdate
from Queries.routeDB import routeGetByLineId

app = Flask(__name__)
api = Api(app, version='1.0', title='Bus Management API',
          description='A simple API for managing buses, drivers, and routes', doc='/swagger/')

ns_driver = api.namespace('drivers', description='Operacje kierowców') #driver
ns_bus = api.namespace('bus', description='Operacje busów') #bus
ns_route = api.namespace('route', description='Operacje kolejności przystanków danej linii') #route line(nazwa, id?) przystanki
ns_trackroute = api.namespace('trackroute', description='O której godzinie dana linii na jakim przystanku odjeżdza') #trackroute
ns_holidays = api.namespace('holidays', description='urlopy') #holiday
ns_track = api.namespace('track', description='Kazdy odjazd danego autobusu z startowej pozycji') #track
ns_combustion = api.namespace('combustion', description='spalanie pojazdu') #
ns_failure_rate = api.namespace('failure_rate', description='jakies raporty')
ns_profitability = api.namespace('profitability', description='jakies raporty - rentownosc')
ns_driver_combustion = api.namespace('driver_combustion', description='spalanie kierowców')

ns_events = api.namespace('events', description='sytuacje specjalne dotyczace autobusów') #eventy

driver_model = api.model('Driver', {
    'name': fields.String(required=True, description='Driver first name'),
    'lastname': fields.String(required=True, description='Driver last name'),
    'license': fields.String(required=True, description='Driver license number'),
    'salary': fields.Float(required=True, description='Driver salary'),
    'holidays_days': fields.Integer(required=True, description='Number of holidays days')
})

bus_model = api.model('Bus', {
    'bus_type_id': fields.Integer(required=True, description='Bus type ID'),
    'next_car_review': fields.String(required=True, description='Next car review date'),
    'actual_event_log_id': fields.Integer(required=True, description='Actual event log ID')
})

#DRIVER API
@ns_driver.route('/get')
class DriverList(Resource):
    def get(self):
        """List all drivers"""
        try:
            return driverGetAll()
        except Exception as e:
            return error(e)

@ns_driver.route('/add')
class DriverAdd(Resource):
    @ns_driver.expect(driver_model)
    def post(self):
        """Add a new driver"""
        try:
            return driverCreate(request.json)
        except Exception as e:
            return error(e)

@ns_driver.route('/get/<int:id>')
class DriverGet(Resource):
    def get(self,id):
        """Get a driver by ID"""
        try:
            return driverGetById(id)
        except Exception as e:
            return error(e)
        
@ns_driver.route('/delete/<int:id>')
class DriverDelete(Resource):
    def delete(self, id):
        """Delete a driver by ID"""
        try:
            return driverDelete(id)
        except Exception as e:
            return error(e)

@ns_driver.route('/update/<int:id>')
class DriverUpdate(Resource):
    @ns_driver.expect(driver_model)
    def put(self, id):
        """Update a driver by ID"""
        try:
            return driverUpdate(request.json, id)
        except Exception as e:
            return error(e)

#BUS API
@ns_bus.route('/get')
class BusList(Resource):
    def get(self):
        """List all buses"""
        try:
            return busGetAll()
        except Exception as e:
            return error(e)

@ns_bus.route('/get/<int:id>')
class BusGet(Resource):
    def get(self, id):
        """"Bus by id"""
        try: 
            return busGetById(id)
        except Exception as e:
            return error(e)

@ns_bus.route('/add')
class BusAdd(Resource):
    @ns_bus.expect(bus_model)
    def post(self):
        """Add a new bus"""
        try:
            return busCreate(request.json)
        except Exception as e:
            return error(e)

@ns_bus.route('/delete/<int:id>')
class BusDelete(Resource):
    def delete(self, id):
        """Delete a bus by ID"""
        try:
            return busDelete()
        except Exception as e:
            return error(e)


@ns_bus.route('/update/<int:id>')
class BusUpdate(Resource):
    @ns_bus.expect(bus_model)
    def put(self, id):
        """Update a bus by ID"""
        try:
            return busUpdate(request.json, id)
        except Exception as e:
            return error(e)

#ROUTE API
@ns_route.route('/get/<int:line_id>')
class RouteList(Resource):
    def get(self, line_id):
        """List all busStop with order for a specific line"""
        try:
            return routeGetByLineId(line_id)
        except Exception as e:
            return error(e)


@ns_trackroute.route('/get/<int:line_id>')
class TrackRoute(Resource):
    def get(self, line_id):
        """Get a specific track route by ID"""
        try:
            connection = create_connection()
            if connection is None:
                return {"error": "Nie udało się połączyć z bazą danych"}, 500

            cursor = connection.cursor()
            query = 'SELECT * FROM public."trackroute" WHERE id = %s'
            cursor.execute(query, (line_id,))
            trackroute = cursor.fetchone()
            cursor.close()
            connection.close()
            return {"trackroute": trackroute}
        except Exception as e:
            print("Wystąpił błąd podczas pobierania danych:", e)
            return {"error": "Wystąpił błąd podczas pobierania danych"}, 500


@ns_holidays.route('/get')
class HolidaysList(Resource):
    def get(self):
        """List all holidays"""
        try:
            connection = create_connection()
            if connection is None:
                return {"error": "Nie udało się połączyć z bazą danych"}, 500

            cursor = connection.cursor()
            query = 'SELECT * FROM public."holidays"'
            cursor.execute(query)
            holidays = cursor.fetchall()
            cursor.close()
            connection.close()
            return {"holidays": holidays}
        except Exception as e:
            print("Wystąpił błąd podczas pobierania danych:", e)
            return {"error": "Wystąpił błąd podczas pobierania danych"}, 500


@ns_holidays.route('/add')
class HolidaysAdd(Resource):
    def post(self):
        """Add a new holiday"""
        try:
            connection = create_connection()
            if connection is None:
                return {"error": "Nie udało się połączyć z bazą danych"}, 500

            cursor = connection.cursor()
            data = request.json
            driver_id = data.get('driver_id')
            start_date = data.get('start_date')
            end_date = data.get('end_date')

            cursor.execute("INSERT INTO holidays (driver_id, start_date, end_date) VALUES "
                           "(%s, %s, %s)", (driver_id, start_date, end_date))
            connection.commit()
            cursor.close()
            connection.close()
            return {"message": "Nowy urlop został dodany pomyślnie"}, 201
        except Exception as e:
            print("Wystąpił błąd podczas dodawania urlopu:", e)
            return {"error": "Wystąpił błąd podczas dodawania urlopu"}, 500


@ns_holidays.route('/delete/<int:driver_id>')
class HolidaysDelete(Resource):
    def delete(self, driver_id):
        """Delete holidays by driver ID"""
        try:
            connection = create_connection()
            if connection is None:
                return {"error": "Nie udało się połączyć z bazą danych"}, 500

            cursor = connection.cursor()
            cursor.execute("DELETE FROM holidays WHERE driver_id = %s", (driver_id,))
            connection.commit()
            cursor.close()
            connection.close()
            return {"message": "Urlop został usunięty pomyślnie"}, 200
        except Exception as e:
            print("Wystąpił błąd podczas usuwania urlopu:", e)
            return {"error": "Wystąpił błąd podczas usuwania urlopu"}, 500


@ns_holidays.route('/update/<int:driver_id>')
class HolidaysUpdate(Resource):
    def put(self, driver_id):
        """Update holidays by driver ID"""
        try:
            if not request.json:
                return {"error": "Nieprawidłowy format danych JSON"}, 400

            data = request.json
            start_date = data.get('start_date')
            end_date = data.get('end_date')

            connection = create_connection()
            if connection is None:
                return {"error": "Nie udało się połączyć z bazą danych"}, 500

            cursor = connection.cursor()
            cursor.execute("""
                UPDATE holidays
                SET start_date = %s, end_date = %s
                WHERE driver_id = %s
            """, (start_date, end_date, driver_id))
            connection.commit()
            cursor.close()
            connection.close()
            return {"message": "Dane urlopu zostały zaktualizowane pomyślnie"}, 200
        except Exception as e:
            print("Wystąpił błąd podczas aktualizowania danych urlopu:", e)
            return {"error": "Wystąpił błąd podczas aktualizowania danych urlopu"}, 500


@ns_events.route('/get')
class EventsList(Resource):
    def get(self):
        """List all events"""
        try:
            connection = create_connection()
            if connection is None:
                return {"error": "Nie udało się połączyć z bazą danych"}, 500

            cursor = connection.cursor()
            query = 'SELECT * FROM public."events"'
            cursor.execute(query)
            events = cursor.fetchall()
            cursor.close()
            connection.close()
            return {"events": events}
        except Exception as e:
            print("Wystąpił błąd podczas pobierania danych:", e)
            return {"error": "Wystąpił błąd podczas pobierania danych"}, 500


@ns_events.route('/add')
class EventsAdd(Resource):
    def post(self):
        """Add a new event"""
        try:
            connection = create_connection()
            if connection is None:
                return {"error": "Nie udało się połączyć z bazą danych"}, 500

            cursor = connection.cursor()
            data = request.json
            bus_id = data.get('bus_id')
            event_type = data.get('event_type')
            event_date = data.get('event_date')

            cursor.execute("INSERT INTO events (bus_id, event_type, event_date) VALUES "
                           "(%s, %s, %s)", (bus_id, event_type, event_date))
            connection.commit()
            cursor.close()
            connection.close()
            return {"message": "Nowe wydarzenie zostało dodane pomyślnie"}, 201
        except Exception as e:
            print("Wystąpił błąd podczas dodawania wydarzenia:", e)
            return {"error": "Wystąpił błąd podczas dodawania wydarzenia"}, 500


@ns_events.route('/delete/<int:id>')
class EventsDelete(Resource):
    def delete(self, id):
        """Delete an event by ID"""
        try:
            connection = create_connection()
            if connection is None:
                return {"error": "Nie udało się połączyć z bazą danych"}, 500

            cursor = connection.cursor()
            cursor.execute("DELETE FROM events WHERE id = %s", (id,))
            connection.commit()
            cursor.close()
            connection.close()
            return {"message": "Wydarzenie zostało usunięte pomyślnie"}, 200
        except Exception as e:
            print("Wystąpił błąd podczas usuwania wydarzenia:", e)
            return {"error": "Wystąpił błąd podczas usuwania wydarzenia"}, 500


@ns_track.route('/get')
class TrackList(Resource):
    def get(self):
        """List all tracks"""
        try:
            connection = create_connection()
            if connection is None:
                return {"error": "Nie udało się połączyć z bazą danych"}, 500

            cursor = connection.cursor()
            query = 'SELECT * FROM public."track"'
            cursor.execute(query)
            tracks = cursor.fetchall()
            cursor.close()
            connection.close()
            return {"tracks": tracks}
        except Exception as e:
            print("Wystąpił błąd podczas pobierania danych:", e)
            return {"error": "Wystąpił błąd podczas pobierania danych"}, 500


@ns_track.route('/add')
class TrackAdd(Resource):
    def post(self):
        """Add a new track"""
        try:
            connection = create_connection()
            if connection is None:
                return {"error": "Nie udało się połączyć z bazą danych"}, 500

            cursor = connection.cursor()
            data = request.json
            route_id = data.get('route_id')
            bus_id = data.get('bus_id')
            driver_id = data.get('driver_id')
            start_time = data.get('start_time')
            end_time = data.get('end_time')

            cursor.execute("INSERT INTO track (route_id, bus_id, driver_id, start_time, end_time) VALUES "
                           "(%s, %s, %s, %s, %s)", (route_id, bus_id, driver_id, start_time, end_time))
            connection.commit()
            cursor.close()
            connection.close()
            return {"message": "Nowy kurs został dodany pomyślnie"}, 201
        except Exception as e:
            print("Wystąpił błąd podczas dodawania kursu:", e)
            return {"error": "Wystąpił błąd podczas dodawania kursu"}, 500


@ns_combustion.route('/get/<int:bus_id>')
class CombustionList(Resource):
    def get(self, bus_id):
        """List all combustions for a specific bus"""
        try:
            connection = create_connection()
            if connection is None:
                return {"error": "Nie udało się połączyć z bazą danych"}, 500

            cursor = connection.cursor()
            query = 'SELECT * FROM public."combustion" WHERE bus_id = %s'
            cursor.execute(query, (bus_id,))
            combustions = cursor.fetchall()
            cursor.close()
            connection.close()
            return {"combustions": combustions}
        except Exception as e:
            print("Wystąpił błąd podczas pobierania danych:", e)
            return {"error": "Wystąpił błąd podczas pobierania danych"}, 500


@ns_failure_rate.route('/get/<int:bus_id>')
class FailureRate(Resource):
    def get(self, bus_id):
        """Get the failure rate for a specific bus"""
        try:
            connection = create_connection()
            if connection is None:
                return {"error": "Nie udało się połączyć z bazą danych"}, 500

            cursor = connection.cursor()
            query = 'SELECT * FROM public."failure_rate" WHERE bus_id = %s'
            cursor.execute(query, (bus_id,))
            failure_rate = cursor.fetchone()
            cursor.close()
            connection.close()
            return {"failure_rate": failure_rate}
        except Exception as e:
            print("Wystąpił błąd podczas pobierania danych:", e)
            return {"error": "Wystąpił błąd podczas pobierania danych"}, 500


@ns_profitability.route('/get/<int:line_id>')
class Profitability(Resource):
    def get(self, line_id):
        """Get the profitability for a specific line"""
        try:
            connection = create_connection()
            if connection is None:
                return {"error": "Nie udało się połączyć z bazą danych"}, 500

            cursor = connection.cursor()
            query = 'SELECT * FROM public."profitability" WHERE line_id = %s'
            cursor.execute(query, (line_id,))
            profitability = cursor.fetchone()
            cursor.close()
            connection.close()
            return {"profitability": profitability}
        except Exception as e:
            print("Wystąpił błąd podczas pobierania danych:", e)
            return {"error": "Wystąpił błąd podczas pobierania danych"}, 500


@ns_driver_combustion.route('/get/<int:driver_id>')
class DriverCombustion(Resource):
    def get(self, driver_id):
        """Get the combustion rate for a specific driver"""
        try:
            connection = create_connection()
            if connection is None:
                return {"error": "Nie udało się połączyć z bazą danych"}, 500

            cursor = connection.cursor()
            query = 'SELECT * FROM public."driver_combustion" WHERE driver_id = %s'
            cursor.execute(query, (driver_id,))
            driver_combustion = cursor.fetchone()
            cursor.close()
            connection.close()
            return {"driver_combustion": driver_combustion}
        except Exception as e:
            print("Wystąpił błąd podczas pobierania danych:", e)
            return {"error": "Wystąpił błąd podczas pobierania danych"}, 500


if __name__ == '__main__':
    app.run(debug=True)
