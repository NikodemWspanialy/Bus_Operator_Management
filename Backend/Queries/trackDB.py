from database import create_connection
from Queries.Extends.responseExtend import concatNameValue, serializeDataTime

def trackGetAll():
  connection = create_connection()
  if connection is None:
    return {"error": "Nie udało się połączyć z bazą danych"}, 500
  cursor = connection.cursor()
  query = """select track.id, line_id, line_name, start_time, bus_type_id from track
left join line on line.id = track.line_id
  """
  cursor.execute(query)
  columns = [desc[0] for desc in cursor.description]
  lines = cursor.fetchall()
  cursor.close()
  connection.close()
  response = concatNameValue(columns, lines)
  response = serializeDataTime(response, 'start_time')
  return {"tracks": response}

def trackGetById(id):
  connection = create_connection()
  if connection is None:
                return {"error": "Nie udało się połączyć z bazą danych"}, 500

  cursor = connection.cursor()
  query = """select track.id, line_id, line_name, start_time, bus_type_id from track
left join line on line.id = track.line_id where track.id = %s"""
  cursor.execute(query, (id,))
  columns = [desc[0] for desc in cursor.description]
  rides = cursor.fetchall()
  cursor.close()
  connection.close()
  response = concatNameValue(columns, rides)
  response = serializeDataTime(response, 'start_time')
  return {"track": response}

def trackCreate(data):
  line = data.get('line_id')
  start_time = data.get('start_time')
  bus_type_id = data.get('bus_type_id')
  connection = create_connection()
  if connection is None:
    return {"error": "Nie udało się połączyć z bazą danych"}, 500

  cursor = connection.cursor()
  query = """INSERT INTO track (line_id, start_time, bus_type_id)
  VALUES (%s, %s, %s)"""
  cursor.execute(query, (line,start_time,bus_type_id ))
  connection.commit()

  query = """select id from track where line_id = %s and start_time = %s and bus_type_id = %s"""
  cursor.execute(query,(line, start_time, bus_type_id))
  ride_id = cursor.fetchall()

  cursor.close()
  connection.close()
  return {"new_track_id": ride_id}, 201


def trackDelete(id):
  connection = create_connection()
  if connection is None:
                return {"error": "Nie udało się połączyć z bazą danych"}, 500

  cursor = connection.cursor()
  cursor.execute("DELETE FROM track WHERE id = %s", (id,))
  connection.commit()
  cursor.close()
  connection.close()
  return {"message": "staly kurs został usunięty pomyślnie"}, 200


def trackUpdate(data, id):
  line = data.get('line_id')
  start_time = data.get('start_time')
  bus_type_id = data.get('bus_type_id')
  connection = create_connection()
  if connection is None:
    return {"error": "Nie udało się połączyć z bazą danych"}, 500

  cursor = connection.cursor()
  cursor.execute("""
    UPDATE track set line_id = %s, start_time = %s, bus_type_id = %s
where id = %s 
    """, (line, start_time, bus_type_id, id))
  connection.commit()
  cursor.close()
  connection.close()
  return {"updated_track_id": id}, 200