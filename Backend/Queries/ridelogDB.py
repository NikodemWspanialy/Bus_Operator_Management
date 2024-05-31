from database import create_connection
from Queries.Extends.responseExtend import concatNameValue, serializeDataTime, serializeDate

def ridelogGetAll():
  connection = create_connection()
  if connection is None:
    return {"error": "Nie udało się połączyć z bazą danych"}, 500
  cursor = connection.cursor()
  query = """select * from ride_log
  """
  cursor.execute(query)
  columns = [desc[0] for desc in cursor.description]
  rides = cursor.fetchall()
  cursor.close()
  connection.close()
  response = concatNameValue(columns, rides)
  return {"ridelogs": response}

def ridelogGetById(id):
  connection = create_connection()
  if connection is None:
                return {"error": "Nie udało się połączyć z bazą danych"}, 500

  cursor = connection.cursor()
  query = """select * from ride_log where id = %s"""
  cursor.execute(query, (id,))
  columns = [desc[0] for desc in cursor.description]
  rides = cursor.fetchall()
  cursor.close()
  connection.close()
  response = concatNameValue(columns, rides)
  return {"ridelog": response}

def ridelogCreate(data):
  ride = data.get('ride_id')
  passengers_number = data.get('passengers_number')
  distance = data.get('distance')
  accident = data.get('accident')

  connection = create_connection()
  if connection is None:
    return {"error": "Nie udało się połączyć z bazą danych"}, 500

  cursor = connection.cursor()
  query = """INSERT INTO ride_log (ride_id, passengers_number, distance, accident)
  VALUES (%s,%s,%s,%s)"""
  cursor.execute(query, (ride, passengers_number, distance, accident))
  connection.commit()

  query = """select id from ride_log where ride_id = %s and passengers_number = %s and distance = %s and accident = %s"""
  cursor.execute(query,(ride, passengers_number, distance, accident))
  ride_id = cursor.fetchall()

  cursor.close()
  connection.close()
  return {"new_ridelog_id": ride_id}, 201


def ridelogDelete(id):
  connection = create_connection()
  if connection is None:
                return {"error": "Nie udało się połączyć z bazą danych"}, 500

  cursor = connection.cursor()
  cursor.execute("DELETE FROM ride_log WHERE id = %s", (id,))
  connection.commit()
  cursor.close()
  connection.close()
  return {"message": "ridelog został usunięty pomyślnie"}, 200


def ridelogUpdate(data, id):
  if not data:
    return {"error": "Nieprawidłowy format danych JSON"}, 400
  ride = data.get('ride_id')
  passengers_number = data.get('passengers_number')
  distance = data.get('distance')
  accident = data.get('accident')
  connection = create_connection()
  if connection is None:
    return {"error": "Nie udało się połączyć z bazą danych"}, 500

  cursor = connection.cursor()
  cursor.execute("""
    UPDATE ride_log set ride_id = %s, passengers_number = %s, distance = %s, accident = %s 
where id = %s 
    """, (ride, passengers_number, distance, accident, id))
  connection.commit()
  cursor.close()
  connection.close()
  return {"updated_ridelog_id": id}, 200