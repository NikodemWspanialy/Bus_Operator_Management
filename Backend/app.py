from flask import Flask, jsonify, request, Blueprint
from flask_cors import CORS
from flask_restx import Api, Resource, fields
from database import error
from QueriesDBImports import *

#flusk API startfile
app = Flask(__name__)
#enable all origins grom all paths
CORS(app, resources={r"/*": {"origins": "*"}})

#swagger
api = Api(app, version='2.0', title='Bus Management API',
          description='SWAGGER ze wszystkimi endpointami restAPI', doc='/swagger/')
#zrobione
ns_driver = api.namespace('drivers', description='CRUD kierowców') 
ns_bus = api.namespace('bus', description='CRUD busow [dla getow rozszerzony o bus-type] ')
ns_route = api.namespace('route', description='zwraca liste wszystkich przystankow dla konkretnej linii [rozszerzony o bus-stop]') 
ns_bus_stop_schedule = api.namespace('bus-stop-schedule', description='zwraca wszystkie odjazdy busow dla tego przystanku (szuka po id)[bazowo jest to klasa trackroute -rozszerzona o route, line, bus-stop]')
ns_holidays = api.namespace('holidays', description='CRUD niedostepnosc kierowcow; w bazie nie ma id wiec poki co nie da sie usuwac i edytowac') #problem z delete i post (pewnie nie bedzie dodane bo nie ma id w bazie narazie), get cos nie dziala?
ns_events = api.namespace('events', description='CRUD tabeli event (zdarzen)')
ns_bus_type = api.namespace('bus-type', description='CRUD tabeli bus_type ; definiuje rodzaje busow oraz ich max. liczbe pasazerow do przewiezienia')
ns_combustion = api.namespace('combustion', description='spalanie pojazdu; przyjmuje id busa i date - zwraca tankowanie ') 
ns_driver_combustion = api.namespace('driver-combustion', description='spalanie kierowców; przyjmuje id kierowcy i date - zwraca tankowanie')
ns_event_log = api.namespace('event-log', description='zdarzenia przypisane do konkretnych busow ; narazie nie edytuje statusu busa - trzeba torobic recznie ') #komentarze w DB
ns_refuiling = api.namespace('refueling', description='CRUD tankowanie')
ns_ride = api.namespace('ride', description='harmonogram przejazdow (nie rozklad jazdy!!!, ta klasa okresla kto i czym jedzie na trasie z tracka) [getery rozszerzone o inne tabele]')
ns_ride_log = api.namespace('ride-log', description='CRUD ride-log [getery rozszerzone o ine tabele]')
ns_line = api.namespace('line', description='CRUD linia ')
ns_track = api.namespace('track', description='track to glowna tabela odjazdow, definiuje ktora linia o ktorej godzinie jedzie (ROZKLAD JAZDY lepiej wyciagnac z bus-stop-schedule)')
ns_bus_stop = api.namespace('bus-stop', description='CRUD dla przystankow')
ns_real_time = api.namespace('real-time', description='tylko gettery bo nie wiem czy bedziemy to recznie robic(powinnien to robic komputer w autobusie na biezaco) [rozszerzone dla czytelnosci]')
#do zaimplementowania
ns_failure_rate = api.namespace('failure-rate', description='raporty - awaryjnosc (potrzebuje feedback czy to tak ma byc)') #bardziej zwraca ride_loga wydaje mi sie trzeba stestowac co i jak
ns_profitability = api.namespace('profitability', description='raporty - rentownosc (nie umiem selecta do tego napisac wiec nie dziala ;( )')

driver_model = api.model('DriverModel', {
    'name': fields.String(required=True, description='imie kierowcy'),
    'lastname': fields.String(required=True, description='nazwisko kierowcy'),
    'license': fields.String(required=True, description='nazwa uprawnien jakie ma kierowca'),
    'salary': fields.Float(required=True, description='wyplata'),
    'holidays_days': fields.Integer(required=True, description='liczba dni wolncy do wykorzystania jeszcze')
})

bus_model = api.model('BusModel', {
    'bus_type_id': fields.Integer(required=True, description='ID typu busa'),
    'next_car_review': fields.String(required=True, description='data nastepnego przegladu'),
    'actual_event_log_id': fields.Integer(required=True, description='jezeli ma jakas uwage, sytuacje to tu powinno byc ID tej sytuacji z tabeli EVENT_LOG, raczej zawsze przy tworzeniu dawac (: null) a ustawiac w ramach pojawienia sie awarii')
})
holiday_model = api.model('HolidayModel', {
    'driver_id': fields.Integer(required=True, description='ID kierowcy'),
    'start_date': fields.String(required=True, description='data rozpoczecia urlopu,zwolnienia itd'),
    'end_date': fields.String(required=True, description='data zakonczenia')
})
event_model = api.model('EventModel', {
    'name': fields.String(required=True, description='nazwa zdarzenia typu: "uszkodzenie - układ chlodzacy"'),
    'description': fields.String(required=True, description='opis doladny typu: "pekniete uszczelka pod glowica"')
})
bus_type_model = api.model('BusTypeModel', {
    'description': fields.String(required=True, description='opis typu na przyklad: standardowy, niskopodlogowy'),
    'shortcut': fields.String(required=True, description='jakis skrot, ktory bedzi widoczny na rozkladzie na przyklad: \'s\''),
    'capacity': fields.Integer(required=True, description='ile osobb sie zmiesci do busa')
})
event_log_model = api.model('eventLogModel',{
    'bus_id': fields.Integer(required=True, description='Id busa'),
    'event_id': fields.Integer(required=True, description='Id eventu'),
    'status': fields.String(required=True, description='jakis opis slowny ktory mozna innym zapytaniem zmieniac zaleznie od statusu np: "in proccess", "ready"'),
    'start_date': fields.String(required=True, description='data rozpoczecia zdarzenia'),
    'end_date': fields.String(required=True, description='data zakonczenia - nie musimy znac, bo nie wiemy kiedy mehanik odda czy cos to dajemy : null (nie \'null\')')
})
event_log_change_status_model = api.model('eventLogEditModel',{
    'status': fields.String(required=True, description='jakis opis slowny ktory mozna innym zapytaniem zmieniac zaleznie od statusu np: "in proccess", "ready"'),
    'end_date': fields.String(required=True, description='data zakonczenia - nie musimy znac, bo nie wiemy kiedy mehanik odda czy cos to dajemy : null (nie \'null\')')
})
refueling_model = api.model('refuelingModel',{
    'bus_id': fields.Integer(required=True, description='id busa'),
    'quantity' : fields.Float(required=True, description='ile litrow'),
    'date': fields.String(required=True, description='data tankowania')
})

ride_model = api.model('rideModel',{
    'bus_id': fields.Integer(required=True, description='id busa, ktora bedzie jechal'),
    'driver_id': fields.Integer(required=True, description='id kirowcy, ktora bedzie jechal'),
    'track_id': fields.Integer(required=True, description='id trasy, tam jest okreslona linia i godzina!'),
    'date': fields.String(required=True, description='data')
})

ridelog_model = api.model('rideLogModel',{
    'ride_id': fields.Integer(required=True, description='ride id'),
    'passengers_number': fields.Integer(required=True, description='liczba pasazerow'),
    'distance': fields.Integer(required=True, description='przejechany dystans'),
    'accident': fields.String(required=True, description='zdarzenie na trasie, wypadek, korki itp, itd - moze byc null jak nic sie nie stalo'),
})

track_model = api.model('trackModel',{
    'line_id': fields.Integer(required=True, description='line id'),
    'start_time': fields.String(required=True, description='godzina odjazdu z przystanku 0'),
    'bus_type_id': fields.Integer(required=True, description='wymagany typ busa na linii')
})
real_time_model = api.model('realTimeModel',{

})
bus_stop_model = api.model('busStopModel',{
    'latitude': fields.Float(required=True, description='wysokosc geograficzna'),
    'longitude': fields.Float(required=True, description='szerokosc geograficzna'),
    'name': fields.String(required=True, description='nazwa przystanku'),
    'adress': fields.String(required=True, description='adres przystanku')
})

#DRIVER API
@ns_driver.route('/get')
class DriverList(Resource):
    def get(self):
        """wylistuj wszystkich kierowcow"""
        try:
            return driverGetAll()
        except Exception as e:
            return error(e)

@ns_driver.route('/add')
class DriverAdd(Resource):
    @ns_driver.expect(driver_model)
    def post(self):
        """dodaj nowego kierowce"""
        try:
            return driverCreate(request.json)
        except Exception as e:
            return error(e)

@ns_driver.route('/get/<int:id>')
class DriverGet(Resource):
    def get(self,id):
        """pobierz kierowce z konkretnym ID"""
        try:
            return driverGetById(id)
        except Exception as e:
            return error(e)
        
@ns_driver.route('/delete/<int:id>')
class DriverDelete(Resource):
    def delete(self, id):
        """Usun kierowce z konkretnym ID"""
        try:
            return driverDelete(id)
        except Exception as e:
            return error(e)

@ns_driver.route('/update/<int:id>')
class DriverUpdate(Resource):
    @ns_driver.expect(driver_model)
    def put(self, id):
        """edytuj kierowce z konkretnyt ID"""
        try:
            return driverUpdate(request.json, id)
        except Exception as e:
            return error(e)

#BUS API
@ns_bus.route('/get')
class BusList(Resource):
    def get(self):
        """Wylistuj wszystkie busy """
        try:
            return busGetAll()
        except Exception as e:
            return error(e)

@ns_bus.route('/get/<int:id>')
class BusGet(Resource):
    def get(self, id):
        """"pobierz busa z konkretnym ID"""
        try: 
            return busGetById(id)
        except Exception as e:
            return error(e)

@ns_bus.route('/add')
class BusAdd(Resource):
    @ns_bus.expect(bus_model)
    def post(self):
        """Dodaj nowy bus (jako maszyna nie linia)"""
        try:
            return busCreate(request.json)
        except Exception as e:
            return error(e)

@ns_bus.route('/delete/<int:id>')
class BusDelete(Resource):
    def delete(self, id):
        """usun bus z konkkretnym ID"""
        try:
            return busDelete()
        except Exception as e:
            return error(e)


@ns_bus.route('/update/<int:id>')
class BusUpdate(Resource):
    @ns_bus.expect(bus_model)
    def put(self, id):
        """Edytuj busa z konkkretnym ID"""
        try:
            return busUpdate(request.json, id)
        except Exception as e:
            return error(e)

#ROUTE API
@ns_route.route('/get/<int:line_id>')
class RouteList(Resource):
    def get(self, line_id):
        """Wylisyuj wszysztkie trasy, czyli wszystkie kolejnsci odjzadow """
        try:
            return routeGetByLineId(line_id)
        except Exception as e:
            return error(e)

#bus_stop_schedule
@ns_bus_stop_schedule.route('/get/<int:id>')
class BusStopDepatureList(Resource):
    def get(self, id):
        """ (ROZKLAD JAZDY DLA PRZYSTRANKU) Wylistuj wszystkie odjzady konkretnych lini z przstanku z ID """
        try:
          return busStopScheduleGetAllByBusStopId(id)
        except Exception as e:
            return error(e)

#holidays / NIEDOSTEPNOSC     
ns_holidays.route('/get/<int:driver_id>')
class HolidaysGet(Resource):
    def get(self, driver_id):
        """Wylistuj wszystkie nieobecnosci kierowcy po jego ID"""
        try:
            return holidaysGetByDriverId(driver_id)
        except Exception as e:
            return error(e)
        
@ns_holidays.route('/get')
class HolidaysList(Resource):
    def get(self):
        """Wylistuj wszystkie nieobecnosci kierowcow"""
        try:
            return holidaysGetAll()
        except Exception as e:
            return error(e)


@ns_holidays.route('/add')
class HolidaysAdd(Resource):
    @ns_holidays.expect(holiday_model)
    def post(self):
        """Dodaj nowy urlop / L4 itd"""
        try:
            return holidaysCreate(request.json)
        except Exception as e:
            return error(e)


@ns_holidays.route('/delete/<int:driver_id>')
class HolidaysDelete(Resource):
    def delete(self, driver_id):
        """Usuń nieobecnosc (nie dizała i nie będzie działać, takze dodawajcie z rozwaga)"""
        try:
            return holidaysDelete(driver_id)
        except Exception as e:
            return error(e)


@ns_holidays.route('/update/<int:driver_id>')
class HolidaysUpdate(Resource):
    @ns_holidays.expect(holiday_model)
    def put(self, driver_id):
        """Edytuj (nie działa)"""
        try:
            return holidaysUpdate(request.json)
        except Exception as e:
           return error(e)

#EVENTY
@ns_events.route('/get')
class EventsList(Resource):
    def get(self):
        """Wylistuj wszystkie typy zdarzen (nie aktulane tylko liste dostepnych zdarzen)"""
        try:
            return eventGetAll()
        except Exception as e:
            return error(e)

@ns_events.route('/add')
class EventsAdd(Resource):
    @ns_events.expect(event_model)
    def post(self):
        """Dodaj nowy typ zdarzenia"""
        try:
            return eventCreate(request.json)
        except Exception as e:
            return error(e)

@ns_events.route('/update/<int:id>')
class EventsAdd(Resource):
    @ns_events.expect(event_model)
    def put(self, id):
        """Edytuj istniejący typ zdarzenia"""
        try:
            return eventUpdate(request.json, id)
        except Exception as e:
            return error(e)

@ns_events.route('/delete/<int:id>')
class EventsDelete(Resource):
    def delete(self, id):
        """usun typ zdarzenia"""
        try:
            return eventDelete(id)
        except Exception as e:
            return error(e)

@ns_events.route('/get/<int:id>')
class EventsGet(Resource):
    def get(self, id):
        """Pobierz typ zdarzenia po ID"""
        try:
            return eventGetById(id)
        except Exception as e:
            return error(e)

#bus type
@ns_bus_type.route('/get')
class BusTypeList(Resource):
    def get(self):
        """Wylistuj wszystkie typy busow"""
        try:
            return busTypeGetAll()
        except Exception as e:
            return error(e)    
        
@ns_bus_type.route('/get/<int:id>')
class BustypeGet(Resource):
    def get(self, id):
        """Pobierz konkretny typ busa po ID"""
        try:
            return busTypeGetById(id)
        except Exception as e:
            return error(e)

@ns_bus_type.route('/delete/<int:id>')
class BusTypeDelete(Resource):
    def delete(self, id):
        """Usun konkretny typ busa"""
        try:
            return busTypeDelete(id)
        except Exception as e:
            return error(e)

@ns_bus_type.route('/add')
class BusTypeAdd(Resource):
    @ns_bus_type.expect(bus_type_model)
    def post(self):
        """DOdaj nowy typ busa"""
        try:
            return busTypeCreate(request.json)
        except Exception as e:
            return error(e)

@ns_bus_type.route('/update/<int:id>')
class BusTypeEdit(Resource):
    @ns_bus_type.expect(bus_type_model)
    def put(self, id):
        """Edytuj typ busa po jego ID"""
        try:
            return busTypeUpdate(request.json, id)
        except Exception as e:
            return error(e)

#spalanie pojazdu 
@ns_combustion.route('/get/<int:bus_id>/<string:data>')
class CombustionList(Resource):
    def get(self, bus_id, data):
        """Parametry spalania konkretnego pojazdu w konkretny dzien (data jako string 'YYYY-MM-DD')"""
        try:
            return combutionGet(bus_id, data)
        except Exception as e:
            return error(e)

#spalanie kierowcow 
@ns_driver_combustion.route('/get/<int:driver_id>/<string:data>')
class DriverCombustion(Resource):
    def get(self, driver_id, data):
        """get spalanie konkretnego kierowcy w konkretny dzien (data jako string 'YYYY-MM-DD')"""
        try:
            return driverCombutionGet(driver_id, data)
        except Exception as e:
            return error(e)


#event log 
@ns_event_log.route('/get')
class EventLog(Resource):
    def get(self):
        """Wylistuj wszystkie"""
        try:
            return eventLogGetAll()
        except Exception as e:
            return error(e)
        
@ns_event_log.route('/get/<int:id>')
class EventLog(Resource):
    def get(self, id):
        """Pobierz zdarzenie po id, potrzebne do wpisania id do bus.actual_event_log_id"""
        try:
            return eventLogGetById(id)
        except Exception as e:
            return error(e)
        

@ns_event_log.route('/get/by-bus/<int:bus_id>')
class EventLog(Resource):
    def get(self, bus_id):
        """Wylistuj cala historie sytuacji awaryjnych konkretnego busa"""
        try:
            return eventLogGetByBusId(bus_id)
        except Exception as e:
            return error(e)
        

@ns_event_log.route('/add')
class EventLog(Resource):
    @ns_event_log.expect(event_log_model)
    def post(self):
        """Dodoaj nowe zdarzenia"""
        try:
            return eventLogCreate(request.json)
        except Exception as e:
            return error(e)

@ns_event_log.route('/edit/<int:id>')
class EventLog(Resource):
    @ns_event_log.expect(event_log_change_status_model)
    def put(self, id):
        """Edytuj zdarzenia"""
        try:
            return eventLogUpdate(id, request.json)
        except Exception as e:
            return error(e)

@ns_event_log.route('/delete/<int:id>')
class EventLog(Resource):
    def delete(self, id):
        """Usun zdarzenia"""
        try:
            return eventLogDelete(id)
        except Exception as e:
            return error(e)

#tankowanie
@ns_refuiling.route('/get')
class Refueling(Resource):
    def get(self):
        """Wylistuj wszystkie tankowania"""
        try:
            return refuelingGetAll()
        except Exception as e:
            return error(e)

@ns_refuiling.route('/get-by-busid/<int:bus_id>')
class Refueling(Resource):
    def get(self, bus_id):
        """Wylistuj wszystkie tankowania konkkretnego busa"""
        try:
            return refuelingGetByBusId(bus_id)
        except Exception as e:
            return error(e)
        
@ns_refuiling.route('/get-by-date/<string:data>')
class Refueling(Resource):
    def get(self, data):
        """Wylistuj wszystkie tankowania po dacie (data jako string 'YYYY-MM-DD')"""
        try:
            return refuelingGetByDate(data)
        except Exception as e:
            return error(e)
        

@ns_refuiling.route('/add')
class Refueling(Resource):
    @ns_refuiling.expect(refueling_model)
    def post(self):
        """Dodaj tankowanie"""
        try:
            return refuelingCreate(request.json)
        except Exception as e:
            return error(e) 

#ride
@ns_ride.route('/get')
class Ride(Resource):
    def get(self):
        """Wylistuj wszystkie przejazdy"""
        try:
            return rideGetAll()
        except Exception as e:
            return error(e)      

@ns_ride.route('/get/<int:id>')
class Ride(Resource):
    def get(self, id):
        """Pobierz przejazd po ID"""
        try:
            return rideGetById(id)
        except Exception as e:
            return error(e) 
        
@ns_ride.route('/get/by-driver/<int:driver_id>')
class Ride(Resource):
    def get(self, driver_id):
        """Pobierz przejazdy po ID kierowcy"""
        try:
            return rideGetByDriverId(driver_id)
        except Exception as e:
            return error(e) 
        
@ns_ride.route('/get/by-date/<string:date>')
class Ride(Resource):
    def get(self, date):
        """Pobierz przejazdy po konkretnej dacie (data jako string 'YYYY-MM-DD')"""
        try:
            return rideGetByDate(date)
        except Exception as e:
            return error(e) 

@ns_ride.route('/add')
class Ride(Resource):
    @ns_ride.expect(ride_model)
    def post(self):
        """Dodaj nowy przejazd"""
        try:
            return rideCreate(request.json)
        except Exception as e:
            return error(e) 

@ns_ride.route('/edit/<int:id>')
class Ride(Resource):
    @ns_ride.expect(ride_model)
    def put(self, id):
        """Edytuj przejazdz z ID"""
        try:
            return rideUpdate(request.json, id)
        except Exception as e:
            return error(e) 

@ns_ride.route('/delete/<int:id>')
class Ride(Resource):
    def delete(self, id):
        """Usun przejazd z ID"""
        try:
            return rideDelete(id)
        except Exception as e:
            return error(e) 


#ridelog
@ns_ride_log.route('/get')
class RideLog(Resource):
    def get(self):
        """Pobierz caly dziennik przejazdow"""
        try:
            return ridelogGetAll()
        except Exception as e:
            return error(e)

@ns_ride_log.route('/get/<int:id>')
class RideLog(Resource):
    def get(self, id):
        """pobierz logi przejazdu o konkretnym ID"""
        try:
            return ridelogGetById(id)
        except Exception as e:
            return error(e)  

@ns_ride_log.route('/delete/<int:id>')
class RideLog(Resource):
    def delete(self, id):
        """Usun log przejazdu - nie uzywac bo nie powino sie"""
        try:
            return ridelogDelete(id)
        except Exception as e:
            return error(e) 

@ns_ride_log.route('/add')
class RideLog(Resource):
    @ns_ride_log.expect(ridelog_model)
    def post(self):
        """Dodaj nowy przejazd - powinny robic sie same"""
        try:
            return ridelogCreate(request.json)
        except Exception as e:
            return error(e) 
        
@ns_ride_log.route('/edit/<int:id>')
class RideLog(Resource):
    @ns_ride_log.expect(ridelog_model)
    def put(self, id):
        """Edytuj przejazd, w ramach dopisania wypadku albo czegos """
        try:
            return ridelogUpdate(request.json, id)
        except Exception as e:
            return error(e) 


#linie ogolnie
@ns_line.route('/get')
class Line(Resource):
    def get(self):
        """Wylistuj wszystkie linie"""
        try:
            return lineGetAll()
        except Exception as e:
            return error(e)
        
@ns_line.route('/get/<int:id>')
class Line(Resource):
    def get(self,id):
        """Pobierz linie po ID"""
        try:
            return lineGetById(id)
        except Exception as e:
            return error(e)
        
@ns_line.route('/get-by-name/<string:name>')
class Line(Resource):
    def get(self,name):
        """Pobierz linie po nazwie"""
        try:
            return lineGetByName(name)
        except Exception as e:
            return error(e)

@ns_line.route('/delete/<int:id>')
class Line(Resource):
    def delete(self,id):
        """usun linie """
        try:
            return lineDelete(id)
        except Exception as e:
            return error(e)
        
@ns_line.route('/add/<string:name>')
class Line(Resource):
    def post(self, name):
        """Dodaj linie"""
        try:
            return lineCreate(name)
        except Exception as e:
            return error(e)
        
@ns_line.route('/edit/<int:id>/<string:name>')
class Line(Resource):
    def put(self, id, name):
        """Edytuj linie - niby put ale mala tabela to wszystko idzie w naglowku, nie ptrzeba wysylac body"""
        try:
            return lineUpdate(id, name)
        except Exception as e:
            return error(e)
#track
@ns_track.route('/get')
class Track(Resource):
    def get(self):
        """Wylisyuj wszysztkie odjzady, czyli wszystkie odjzady wszystkich lini z przystanku startowego dla tej linii """
        try:
            return trackGetAll()
        except Exception as e:
            return error(e)

@ns_track.route('/get/<int:id>')
class Track(Resource):
    def get(self, id):
        """Pobierz konkretny odjazd, po ID"""
        try:
            return trackGetById(id)
        except Exception as e:
            return error(e)

@ns_track.route('/delete/<int:id>')
class Track(Resource):
    def delete(self, id):
        """Usun odjazd"""
        try:
            return trackDelete(id)
        except Exception as e:
            return error(e)

@ns_track.route('/add')
class Track(Resource):
    @ns_track.expect(track_model)
    def post(self):
        """Dodaj nowy odjzad"""
        try:
            return trackCreate(request.json)
        except Exception as e:
            return error(e)

@ns_track.route('/edit/<int:id>')
class Track(Resource):
    @ns_track.expect(track_model)
    def put(self,id):
        """Edytuj odjzad"""
        try:
            return trackUpdate(request.json, id)
        except Exception as e:
            return error(e)

#przystanki 
@ns_bus_stop.route('/get')
class BusStop(Resource):
    def get(self):
        """Wylistuj wszystkie przystanki"""
        try:
            return busstopGetAll()
        except Exception as e:
            return error(e)

@ns_bus_stop.route('/get/<int:id>')
class BusStop(Resource):
    def get(self, id):
        """Pobierz przystanek po ID"""
        try:
            return busstopGetById(id)
        except Exception as e:
            return error(e)

@ns_bus_stop.route('/get-by-name/<string:name>')
class BusStop(Resource):
    def get(self, name):
        """Piberz przystanek po nazwie"""
        try:
            return busstopGetByName(name)
        except Exception as e:
            return error(e)

@ns_bus_stop.route('/delete/<int:id>')
class BusStop(Resource):
    def delete(self, id):
        """Usun przystanek"""
        try:
            return busstopDelete(id)
        except Exception as e:
            return error(e)

@ns_bus_stop.route('/add')
class BusStop(Resource):
    @ns_bus_stop.expect(bus_stop_model)
    def post(self):
        """Dodaj nowy przystanek"""
        try:
            return busstopCreate(request.json)
        except Exception as e:
            return error(e)

@ns_bus_stop.route('/edit/<int:id>')
class BusStop(Resource):
    @ns_bus_stop.expect(bus_stop_model)
    def put(self,id):
        """Edytuj przystanek"""
        try:
            return busstopUpdate(request.json, id)
        except Exception as e:
            return error(e)
 
#real time    
@ns_real_time.route('/get')
class RealTime(Resource):
    def get(self):
        """Pobierz wszystkie opoznienia, przyspieszenia"""
        try:
            return realtimeGetAll()
        except Exception as e:
            return error(e)
        
@ns_real_time.route('/get/<int:trackroute_id>')
class RealTime(Resource):
    def get(self, trackroute_id):
        """Pobierz opznienia dla konkretnego przystanku (moze byc pare rekordow , kazdy dla nnego dnia jest, ale w bazie sa tylko na jeden dzien zrobione bo duzo roboty to bylo)"""
        try:
            return realtimeGetById(trackroute_id)
        except Exception as e:
            return error(e)
        
@ns_real_time.route('/get-by-ride-id/<int:ride_id>')
class RealTime(Resource):
    def get(self, ride_id):
        """Pobierz opznienia dla konkretnego kursu, czyli liczba rekordow bedzie rowna ilosci przystankow, jakie ma linia """
        try:
            return realtimeGetByRideId(ride_id)
        except Exception as e:
            return error(e)

#################################
### tu zaczac nastepnym razem ###
#################################

#awaryjnosc - dodac dla wszystkich lacznie, dla pojedynczego wylistowane, dla jednego by ID
@ns_failure_rate.route('/get/<int:bus_id>/<string:date>')
class FailureRate(Resource):
    def get(self, bus_id, date):
        """Pobierz awaryjnosc dla busa i daty - 'RRRR-MM-DD'"""
        try:
            return failureGetAllById(bus_id, date)
        except Exception as e:
            return error(e)
        
@ns_failure_rate.route('/get/<string:date>')
class FailureRate(Resource):
    def get(self, date):
        """Pobierz awaryjnsci dla busow w konkretnej dacie"""
        try:
            return failureGetAll(date)
        except Exception as e:
            return error(e)
        
@ns_failure_rate.route('/get-accidents-only/<int:bus_id>/<string:date>')
class FailureRate(Resource):
    def get(self, bus_id, date):
        """Pobierz awaryjnosci dla busa i daty, wyswieltli tylko rekordy z zsarzeniam"""
        try:
            return failureGetById(bus_id, date)
        except Exception as e:
            return error(e)
        
@ns_failure_rate.route('/get-accidents-only/<string:date>')
class FailureRate(Resource):
    def get(self, date):
        """Pobierz awaryjnosci dla wszystkich busow i konkretnej daty, wyswieltli tylko rekordy z zsarzeniam"""
        try:
            return failureGet(date)
        except Exception as e:
            return error(e)


#renotownosc linii
@ns_profitability.route('/get/<int:line_id>')
class Profitability(Resource):
    def get(self, line_id):
        """Pobierz rentownosc linii po jej ID - nie dizala"""
        try:
            raise NotImplementedError('not implemented')
        except Exception as e:
            return error(e)

@ns_profitability.route('/get')
class Profatibility(Resource):
    def get(self):
        """Pobierz wszystkie rentownosci"""
        try:
            raise NotImplementedError('not implemented')
        except Exception as e:
            return error(e)


if __name__ == '__main__':
    app.run(debug=True)