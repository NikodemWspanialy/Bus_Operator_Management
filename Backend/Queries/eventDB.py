from database import create_connection
from Queries.Extends.responseExtend import concatNameValue

def eventGetAll():
  connection = create_connection()
  if connection is None:
    return {"error": "Nie udało się połączyć z bazą danych"}, 500
  cursor = connection.cursor()
  query = 'SELECT * FROM event'
  cursor.execute(query)
  columns = [desc[0] for desc in cursor.description]
  events = cursor.fetchall()
  cursor.close()
  connection.close()
  response = concatNameValue(columns, events)
  return {"events": response}

def eventGetById(id):
  connection = create_connection()
  if connection is None:
                return {"error": "Nie udało się połączyć z bazą danych"}, 500

  cursor = connection.cursor()
  query = 'SELECT * FROM event WHERE id = %s'
  cursor.execute(query, (id,))
  columns = [desc[0] for desc in cursor.description]
  events = cursor.fetchall()
  cursor.close()
  connection.close()
  response = concatNameValue(columns, events)
  return {"event": response}


def eventCreate(data):
  name = data.get('name')
  description = data.get('description')
  connection = create_connection()
  if connection is None:
    return {"error": "Nie udało się połączyć z bazą danych"}, 500
  cursor = connection.cursor()
  cursor.execute("INSERT INTO event (name, description) VALUES (%s, %s, %s, %s, %s)", (name, description))
  connection.commit()
  query = 'SELECT id FROM event where name=%s and description=%s'
  cursor.execute(query,(name, description))
  event_id = cursor.fetchall()
  cursor.close()
  connection.close()
  return {"new_event_id": event_id}, 201


def eventDelete(id):
  connection = create_connection()
  if connection is None:
                return {"error": "Nie udało się połączyć z bazą danych"}, 500

  cursor = connection.cursor()
  cursor.execute("DELETE FROM event WHERE id = %s", (id,))
  connection.commit()
  cursor.close()
  connection.close()
  return {"message": "event został usunięty pomyślnie"}, 200


def eventUpdate(data, id):
  if not data:
    return {"error": "Nieprawidłowy format danych JSON"}, 400

  name = data.get('name')
  description = data.get('description')

  if not all([name, description]):
   return {"error": "Brak wymaganych pól"}, 400

  connection = create_connection()
  if connection is None:
    return {"error": "Nie udało się połączyć z bazą danych"}, 500

  cursor = connection.cursor()
  cursor.execute("""
    UPDATE event SET name = %s, description = %s WHERE id = %s
    """, (name, description, id))
  connection.commit()
  query = 'Select id from event where name = %s and lastname = %s'
  event_id = cursor.execute(query, (name, description))
  cursor.close()
  connection.close()
  return {"updated_event_id": event_id}, 200