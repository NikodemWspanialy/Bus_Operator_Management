from database import create_connection
from Queries.Extends.responseExtend import concatNameValue, serializeDataTime

def busstopGetAll():
  connection = create_connection()
  if connection is None:
    return {"error": "Nie udało się połączyć z bazą danych"}, 500
  cursor = connection.cursor()
  query = """select * from bus_stop
  """
  cursor.execute(query)
  columns = [desc[0] for desc in cursor.description]
  lines = cursor.fetchall()
  cursor.close()
  connection.close()
  response = concatNameValue(columns, lines)
  return {"bus_stops": response}

def busstopGetById(id):
  connection = create_connection()
  if connection is None:
                return {"error": "Nie udało się połączyć z bazą danych"}, 500

  cursor = connection.cursor()
  query = """select * from bus_stop where id = %s"""
  cursor.execute(query, (id,))
  columns = [desc[0] for desc in cursor.description]
  rides = cursor.fetchall()
  cursor.close()
  connection.close()
  response = concatNameValue(columns, rides)
  return {"bus_stop": response}

def busstopGetByName(name):
  connection = create_connection()
  if connection is None:
                return {"error": "Nie udało się połączyć z bazą danych"}, 500

  cursor = connection.cursor()
  query = """select * from bus_stop where name = %s"""
  cursor.execute(query, (name,))
  columns = [desc[0] for desc in cursor.description]
  rides = cursor.fetchall()
  cursor.close()
  connection.close()
  response = concatNameValue(columns, rides)
  return {"bus_stop": response}

def busstopCreate(data):
  latitude = data.get('latitude')
  longitude = data.get('longitude')
  name = data.get('name')
  adress = data.get('adress')
  connection = create_connection()
  if connection is None:
    return {"error": "Nie udało się połączyć z bazą danych"}, 500

  cursor = connection.cursor()
  query = """INSERT INTO bus_stop (latitude, longitude, name,adress)
  VALUES (%s, %s, %s,%s)"""
  cursor.execute(query, (latitude,longitude,name,adress ))
  connection.commit()

  query = """select id from bus_stop where name = %s and adress = %s and latitude = %s"""
  cursor.execute(query,(name, adress, latitude))
  ride_id = cursor.fetchall()

  cursor.close()
  connection.close()
  return {"new_bus_stop_id": ride_id}, 201


def busstopDelete(id):
  connection = create_connection()
  if connection is None:
                return {"error": "Nie udało się połączyć z bazą danych"}, 500

  cursor = connection.cursor()
  cursor.execute("DELETE FROM bus_stop WHERE id = %s", (id,))
  connection.commit()
  cursor.close()
  connection.close()
  return {"message": "przystanek został usunięty pomyślnie"}, 200


def busstopUpdate(data, id):
  latitude = data.get('latitude')
  longitude = data.get('longitude')
  name = data.get('name')
  adress = data.get('adress')
  connection = create_connection()
  if connection is None:
    return {"error": "Nie udało się połączyć z bazą danych"}, 500

  cursor = connection.cursor()
  cursor.execute("""
    UPDATE bus_stop set latitude = %s, longitude = %s, name = %s, adress = %s
where id = %s 
    """, (latitude, longitude, name,adress, id))
  connection.commit()
  cursor.close()
  connection.close()
  return {"updated_bus_stop_id": id}, 200