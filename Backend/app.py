from flask import Flask, jsonify, request
from flask_restx import Api, Resource, fields
from database import create_connection, error
from Queries.driverDB import driverGetAll, driverCreate, driverGetById, driverDelete, driverUpdate
from Queries.BusDB import busGetAll, busCreate, busDelete, busGetById, busUpdate
from Queries.routeDB import routeGetByLineId
from Queries.busStopScheduleDB import busStopScheduleGetAllByBusStopId
from Queries.HolidaysDB import holidaysCreate, holidaysDelete,holidaysGetAll, holidaysGetByDriverId, holidaysUpdate
from Queries.eventDB import eventGetAll, eventCreate, eventDelete, eventGetById, eventUpdate

app = Flask(__name__)
api = Api(app, version='1.0', title='Bus Management API',
          description='A simple API for managing buses, drivers, and routes', doc='/swagger/')
#zrobione
ns_driver = api.namespace('drivers', description='Operacje kierowców') #driver
ns_bus = api.namespace('bus', description='Operacje busów') #bus
ns_route = api.namespace('route', description='Operacje kolejności przystanków danej linii') #route line(nazwa, id?) przystanki
ns_bus_stop_schedule = api.namespace('bus_stop_schedule', description='odjazdy  z przystanku(id) busow')
ns_holidays = api.namespace('holidays', description='urlopy') #holiday
ns_events = api.namespace('events', description='sytuacje specjalne dotyczace autobusów') #eventy
#do zaimplementowania
ns_bus_type = api.namespace('bus_type', description='rodzaje busow')
ns_combustion = api.namespace('combustion', description='spalanie pojazdu') 
ns_driver_combustion = api.namespace('driver_combustion', description='spalanie kierowców')
ns_profitability = api.namespace('profitability', description='raporty - rentownosc')
ns_failure_rate = api.namespace('failure_rate', description='awaryjnosc raporty')
#do zrobienia
ns_event_log = api.namespace('event_log', description='zdarzenia przypisane do konkretnych busow')
ns_refuiling = api.namespace('refueling', description='tankowanie')
ns_ride = api.namespace('ride', description='przejazdy z kierowca, busem, linia, data')
ns_ride_log = api.namespace('ride_log', description='cala historia przejazdow z parametrami')

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

#bus_stop_schedule
@ns_bus_stop_schedule.route('/get/<int:id>')
class BusStopDepatureList(Resource):
    def get(self, id):
        """Get all depature from specify bus stop"""
        try:
          return busStopScheduleGetAllByBusStopId(id)
        except Exception as e:
            return error(e)

#holidays / NIEDOSTEPNOSC     
ns_holidays.route('/get/<int:id>')
class HolidaysGet(Resource):
    def get(self, id):
        """Get holidays by driver_id"""
        try:
            return holidaysGetByDriverId(id)
        except Exception as e:
            return error(e)
        
@ns_holidays.route('/get')
class HolidaysList(Resource):
    def get(self):
        """List all holidays"""
        try:
            return holidaysGetAll()
        except Exception as e:
            return error(e)


@ns_holidays.route('/add')
class HolidaysAdd(Resource):
    def post(self):
        """Add a new holiday"""
        try:
            return holidaysCreate(request.json)
        except Exception as e:
            return error(e)


@ns_holidays.route('/delete/<int:driver_id>')
class HolidaysDelete(Resource):
    def delete(self, driver_id):
        """Delete holidays by driver ID"""
        try:
            return holidaysDelete(driver_id)
        except Exception as e:
            return error(e)


@ns_holidays.route('/update/<int:driver_id>')
class HolidaysUpdate(Resource):
    def put(self, driver_id):
        """Update holidays by driver_ID"""
        try:
            return holidaysUpdate(request.json)
        except Exception as e:
           return error(e)

#EVENTY
@ns_events.route('/get')
class EventsList(Resource):
    def get(self):
        """List all events"""
        try:
            return eventGetAll()
        except Exception as e:
            return error(e)

@ns_events.route('/add')
class EventsAdd(Resource):
    def post(self):
        """Add a new event"""
        try:
            return eventCreate(request.json)
        except Exception as e:
            return error(e)

@ns_events.route('/update/<int:id>')
class EventsAdd(Resource):
    def put(self, id):
        """Update event by specify Id"""
        try:
            return eventUpdate(request.json, id)
        except Exception as e:
            return error(e)

@ns_events.route('/delete/<int:id>')
class EventsDelete(Resource):
    def delete(self, id):
        """Delete an event by ID"""
        try:
            return eventDelete(id)
        except Exception as e:
            return error(e)

@ns_events.route('/get/<int:id>')
class EventsGet(Resource):
    def get(self, id):
        """Get event by id"""
        try:
            return eventGetById(id)
        except Exception as e:
            return error(e)

#################################
### tu zaczac nastepnym razem ###
#################################

#bus type
@ns_bus_type.route('/get')
class BusTypeList(Resource):
    def get(self):
        """List all bus type"""
        try:
            raise NotImplementedError
        except Exception as e:
            return error(e)    
        
@ns_bus_type.route('/get/<int:id>')
class BustypeGet(Resource):
    def get(self, id):
        """get specify bus type by id"""
        try:
            raise NotImplementedError
        except Exception as e:
            return error(e)

@ns_bus_type.route('/delete/<int:id>')
class BusTypeDelete(Resource):
    def delete(self, id):
        """delete bus with id"""
        try:
            raise NotImplementedError
        except Exception as e:
            return error(e)

@ns_bus_type.route('/add')
class BusTypeAdd(Resource):
    def post(self):
        """Create a new bus type"""
        try:
            raise NotImplementedError
        except Exception as e:
            return error(e)

@ns_bus_type.route('/update/<int:id>')
class BusTypeEdit(Resource):
    def post(self, id):
        """edit specify bus typw with id"""
        try:
            raise NotImplementedError
        except Exception as e:
            return error(e)

#spalanie pojazdu 
@ns_combustion.route('/get/<int:bus_id>')
class CombustionList(Resource):
    def get(self, bus_id):
        """Parametry spalania kazdego pojazdu """
        try:
            raise NotImplementedError
        except Exception as e:
            return error(e)

#spalanie kierowcow 
@ns_driver_combustion.route('/get/<int:driver_id>')
class DriverCombustion(Resource):
    def get(self, driver_id):
        """get spalaanie kierowcy"""
        try:
            raise NotImplementedError
        except Exception as e:
            return error(e)

#renotownosc linii
@ns_profitability.route('/get/<int:line_id>')
class Profitability(Resource):
    def get(self, line_id):
        """Get rentownosc linii po Id linii"""
        try:
            raise NotImplementedError
        except Exception as e:
            return error(e)

@ns_profitability.route('/get')
class Profatibility(Resource):
    def get(self):
        """Get rentownosc linii wszystkich"""
        try:
            raise NotImplementedError
        except Exception as e:
            return error(e)

#awaryjnosc - dodac dla wszystkich lacznie, dla pojedynczego wylistowane, dla jednego by ID
@ns_failure_rate.route('/get/<int:bus_id>')
class FailureRate(Resource):
    def get(self, bus_id):
        """Get the awaryjnosc rate for a specific bus"""
        try:
            raise NotImplementedError
        except Exception as e:
            return error(e)
        
@ns_failure_rate.route('/get')
class FailureRate(Resource):
    def get(self):
        """Get the awaryjnosc rate for every bus"""
        try:
            raise NotImplementedError
        except Exception as e:
            return error(e)

if __name__ == '__main__':
    app.run(debug=True)
