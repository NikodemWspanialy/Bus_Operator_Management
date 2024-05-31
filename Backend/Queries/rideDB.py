from database import create_connection
from Queries.Extends.responseExtend import concatNameValue, serializeDataTime, serializeDate

def rideGetAll():
  connection = create_connection()
  if connection is None:
    return {"error": "Nie udało się połączyć z bazą danych"}, 500
  cursor = connection.cursor()
  query = """
  select r.id as ride_id, r.bus_id, r.track_id, tr.line_id, l.line_name, date, tr.start_time, r.driver_id, d.name as driver_name, d.lastname as driver_lastname  from ride r
inner join track tr on tr.id = r.track_id 
inner join line l on l.id = tr.line_id
inner join bus b on b.id = r.bus_id
inner join driver d on d.id = r.driver_id
order by date, start_time"""
  cursor.execute(query)
  columns = [desc[0] for desc in cursor.description]
  rides = cursor.fetchall()
  cursor.close()
  connection.close()
  response = concatNameValue(columns, rides)
  response = serializeDataTime(response, 'start_time')
  response = serializeDate(response, 'date')
  return {"rides": response}

def rideGetById(id):
  connection = create_connection()
  if connection is None:
                return {"error": "Nie udało się połączyć z bazą danych"}, 500

  cursor = connection.cursor()
  query = """select r.id as ride_id, r.bus_id, r.track_id, tr.line_id, l.line_name, date, tr.start_time, r.driver_id, d.name as driver_name, d.lastname as driver_lastname  from ride r
inner join track tr on tr.id = r.track_id 
inner join line l on l.id = tr.line_id
inner join bus b on b.id = r.bus_id
inner join driver d on d.id = r.driver_id
where r.id = %s
order by date, start_time"""
  cursor.execute(query, (id,))
  columns = [desc[0] for desc in cursor.description]
  rides = cursor.fetchall()
  cursor.close()
  connection.close()
  response = concatNameValue(columns, rides)
  response = serializeDataTime(response, 'start_time')
  response = serializeDate(response, 'date')
  return {"ride": response}

def rideGetByDate(date):
  connection = create_connection()
  if connection is None:
                return {"error": "Nie udało się połączyć z bazą danych"}, 500

  cursor = connection.cursor()
  query = """select r.id as ride_id, r.bus_id, r.track_id, tr.line_id, l.line_name, date, tr.start_time, r.driver_id, d.name as driver_name, d.lastname as driver_lastname  from ride r
inner join track tr on tr.id = r.track_id 
inner join line l on l.id = tr.line_id
inner join bus b on b.id = r.bus_id
inner join driver d on d.id = r.driver_id
where r.date = %s
order by date, start_time"""
  cursor.execute(query, (date,))
  columns = [desc[0] for desc in cursor.description]
  rides = cursor.fetchall()
  cursor.close()
  connection.close()
  response = concatNameValue(columns, rides)
  response = serializeDataTime(response, 'start_time')
  response = serializeDate(response, 'date')
  return {"ride": response}

def rideGetByDriverId(id):
  connection = create_connection()
  if connection is None:
                return {"error": "Nie udało się połączyć z bazą danych"}, 500

  cursor = connection.cursor()
  query = """select r.id as ride_id, r.bus_id, r.track_id, tr.line_id, l.line_name, date, tr.start_time, r.driver_id, d.name as driver_name, d.lastname as driver_lastname  from ride r
inner join track tr on tr.id = r.track_id 
inner join line l on l.id = tr.line_id
inner join bus b on b.id = r.bus_id
inner join driver d on d.id = r.driver_id
where r.driver_id = %s
order by date, start_time"""
  cursor.execute(query, (id,))
  columns = [desc[0] for desc in cursor.description]
  rides = cursor.fetchall()
  cursor.close()
  connection.close()
  response = concatNameValue(columns, rides)
  response = serializeDataTime(response, 'start_time')
  response = serializeDate(response, 'date')
  return {"ride": response}


def rideCreate(data):
  driver = data.get('driver_id')
  bus = data.get('bus_id')
  track = data.get('track_id')
  date = data.get('date')

  connection = create_connection()
  if connection is None:
    return {"error": "Nie udało się połączyć z bazą danych"}, 500

  cursor = connection.cursor()
  query = """INSERT INTO ride (bus_id, driver_id, track_id, date)
  VALUES (%s,%s,%s,%s)"""
  cursor.execute(query, (bus, driver, track, date))
  connection.commit()

  query = """select id from ride where bus_id = %s and driver_id = %s and track_id = %s and date = %s"""
  cursor.execute(query,(bus, driver, track, date))
  ride_id = cursor.fetchall()

  cursor.close()
  connection.close()
  return {"new_ride_id": ride_id}, 201


def rideDelete(id):
  connection = create_connection()
  if connection is None:
                return {"error": "Nie udało się połączyć z bazą danych"}, 500

  cursor = connection.cursor()
  cursor.execute("DELETE FROM ride WHERE id = %s", (id,))
  connection.commit()
  cursor.close()
  connection.close()
  return {"message": "jazda został usunięty pomyślnie"}, 200


def rideUpdate(data, id):
  if not data:
    return {"error": "Nieprawidłowy format danych JSON"}, 400
  driver = data.get('driver_id')
  bus = data.get('bus_id')
  track = data.get('track_id')
  date = data.get('date')
  connection = create_connection()
  if connection is None:
    return {"error": "Nie udało się połączyć z bazą danych"}, 500

  cursor = connection.cursor()
  cursor.execute("""
    UPDATE ride set bus_id = %s, driver_id = %s, track_id = %s, date = %s 
where id = %s 
    """, (bus, driver, track, date, id))
  connection.commit()
  cursor.close()
  connection.close()
  return {"updated_ride_id": id}, 200