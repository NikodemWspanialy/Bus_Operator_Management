from database import create_connection
from Queries.Extends.responseExtend import concatNameValue

def busGetAll():
  connection = create_connection()
  if connection is None:
    return {"error": "Nie udało się połączyć z bazą danych"}, 500
  cursor = connection.cursor()
  query = 'SELECT b.id, bt.description, bt.shortcut, capacity FROM bus b inner join bus_type bt on bt.id = b.bus_type_id '
  cursor.execute(query)
  buses = cursor.fetchall()
  columns = [desc[0] for desc in cursor.description]
  cursor.close()
  connection.close()
  response = concatNameValue(columns, buses)
  return {"buses": response}

def busGetById(id):
  connection = create_connection()
  if connection is None:
    return {"error": "Nie udało się połączyć z bazą danych"}, 500
  cursor = connection.cursor()
  query = 'SELECT b.id, bt.description, bt.shortcut, capacity FROM bus b inner join bus_type bt on bt.id = b.bus_type_id where b.id =  %s'
  cursor.execute(query, (id,))
  bus = cursor.fetchall()
  columns = [desc[0] for desc in cursor.description]
  response = concatNameValue(columns, bus)
  return{"bus": response}

def busDelete(id):
  connection = create_connection()
  if connection is None:
     return {"error": "Nie udało się połączyć z bazą danych"}, 500

  cursor = connection.cursor()
  cursor.execute("DELETE FROM bus WHERE id = %s", (id,))
  connection.commit()
  cursor.close()
  connection.close()
  return {"message": "Autobus został usunięty pomyślnie"}, 200

def busUpdate(data, id):
  if not data:
    return {"error": "Nieprawidłowy format danych JSON"}, 400

  bus_type_id = data.get('bus_type_id')
  next_car_review = data.get('next_car_review')
  actual_event_log_id = data.get('actual_event_log_id')
  if not all([bus_type_id, next_car_review]):
    return {"error": "Brak wymaganych pól"}, 400

  connection = create_connection()
  if connection is None:
    return {"error": "Nie udało się połączyć z bazą danych"}, 500
  cursor = connection.cursor()
  cursor.execute("""
                UPDATE bus
                SET bus_type_id = %s, next_car_review = %s, actual_event_log_id = %s
                WHERE id = %s
            """, (bus_type_id, next_car_review, actual_event_log_id, id))
  connection.commit()
  cursor.close()
  connection.close()
  return {"message": "Dane autobusu zostały zaktualizowane pomyślnie"}, 200

def busCreate(data):
  connection = create_connection()
  if connection is None:
    return {"error": "Nie udało się połączyć z bazą danych"}, 500
  cursor = connection.cursor()
  bus_type_id = data.get('bus_type_id')
  next_car_review = data.get('next_car_review')
  actual_event_log_id = data.get('actual_event_log_id')

  cursor.execute("INSERT INTO bus (bus_type_id, next_car_review, actual_event_log_id) VALUES (%s, %s, %s)", (bus_type_id, next_car_review, actual_event_log_id))
  connection.commit()
  cursor.close()
  connection.close()
  return {"message": "Nowy autobus został dodany pomyślnie"}, 201