from database import create_connection
from Queries.Extends.responseExtend import concatNameValue, serializeDataTime, serializeDate

def realtimeGetAll():
  connection = create_connection()
  if connection is None:
    return {"error": "Nie udało się połączyć z bazą danych"}, 500
  cursor = connection.cursor()
  query = """select ride_id, track_route_id, time as scheduled_time, real_time, r.date from real_time_trackroute rt
inner join trackroute tr on tr.id = rt.track_route_id
inner join ride r on r.id = rt.ride_id
  """
  cursor.execute(query)
  columns = [desc[0] for desc in cursor.description]
  lines = cursor.fetchall()
  cursor.close()
  connection.close()
  response = concatNameValue(columns, lines)
  response = serializeDataTime(response, 'scheduled_time')
  response = serializeDataTime(response, 'real_time')
  response = serializeDate(response, 'date')
  return {"realtimes": response}

def realtimeGetById(id):
  connection = create_connection()
  if connection is None:
                return {"error": "Nie udało się połączyć z bazą danych"}, 500

  cursor = connection.cursor()
  query = """select ride_id, track_route_id, time as scheduled_time, real_time, r.date from real_time_trackroute rt
inner join trackroute tr on tr.id = rt.track_route_id
inner join ride r on r.id = rt.ride_id
where tr.id = %s"""
  cursor.execute(query, (id,))
  columns = [desc[0] for desc in cursor.description]
  rides = cursor.fetchall()
  cursor.close()
  connection.close()
  response = concatNameValue(columns, rides)
  response = serializeDataTime(response, 'scheduled_time')
  response = serializeDataTime(response, 'real_time')
  response = serializeDate(response, 'date')
  return {"realtime": response}

def realtimeGetByRideId(id):
  connection = create_connection()
  if connection is None:
                return {"error": "Nie udało się połączyć z bazą danych"}, 500

  cursor = connection.cursor()
  query = """select ride_id, track_route_id, time as scheduled_time, real_time, r.date from real_time_trackroute rt
inner join trackroute tr on tr.id = rt.track_route_id
inner join ride r on r.id = rt.ride_id
where r.id = %s"""
  cursor.execute(query, (id,))
  columns = [desc[0] for desc in cursor.description]
  rides = cursor.fetchall()
  cursor.close()
  connection.close()
  response = concatNameValue(columns, rides)
  response = serializeDataTime(response, 'scheduled_time')
  response = serializeDataTime(response, 'real_time')
  response = serializeDate(response, 'date')
  return {"realtimes": response}

