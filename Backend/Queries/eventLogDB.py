from database import create_connection
from Queries.Extends.responseExtend import concatNameValue, serializeDate

def eventLogGetAll():
  connection = create_connection()
  if connection is None:
    return {"error": "Nie udało się połączyć z bazą danych"}, 500
  cursor = connection.cursor()
  query = 'SELECT * FROM event_log'
  cursor.execute(query)
  columns = [desc[0] for desc in cursor.description]
  drivers = cursor.fetchall()
  cursor.close()
  connection.close()
  response = concatNameValue(columns, drivers)
  response = serializeDate(response, 'start_date')
  response = serializeDate(response, 'end_date')
  return {"eventLogs": response}

def eventLogGetById(id):
  connection = create_connection()
  if connection is None:
                return {"error": "Nie udało się połączyć z bazą danych"}, 500

  cursor = connection.cursor()
  query = 'SELECT * FROM event_log WHERE id = %s'
  cursor.execute(query, (id,))
  columns = [desc[0] for desc in cursor.description]
  driver = cursor.fetchall()
  cursor.close()
  connection.close()
  response = concatNameValue(columns, driver)
  response = serializeDate(response, 'start_date')
  response = serializeDate(response, 'end_date')
  return {"eventLog": response}

def eventLogGetByBusId(id):
  connection = create_connection()
  if connection is None:
                return {"error": "Nie udało się połączyć z bazą danych"}, 500

  cursor = connection.cursor()
  query = 'SELECT * FROM event_log WHERE bus_id = %s'
  cursor.execute(query, (id,))
  columns = [desc[0] for desc in cursor.description]
  driver = cursor.fetchall()
  cursor.close()
  connection.close()
  response = concatNameValue(columns, driver)
  response = serializeDate(response, 'start_date')
  response = serializeDate(response, 'end_date')
  return {"eventLog": response}

def eventLogCreate(data):
  bus_id = data.get('bus_id')
  event_id = data.get('event_id')
  status = data.get('status')
  start_date = data.get('start_date')
  end_date = data.get('end_date')
  connection = create_connection()
  if connection is None:
    return {"error": "Nie udało się połączyć z bazą danych"}, 500
  cursor = connection.cursor()
  cursor.execute("INSERT INTO event_log (bus_id, event_id, status, start_date, end_date) VALUES (%s, %s, %s, %s, %s)", (bus_id, event_id, status, start_date, end_date))
  connection.commit()
  query = 'SELECT id FROM event_log where bus_id=%s and event_id=%s'
  cursor.execute(query,(bus_id, event_id))
  eventlog_id = cursor.fetchall()
  #new_event_log_id = event_id[0]
  #query2 = """update bus set actual_event_log_id = %s
  #where id = %s"""
  #cursor.execute(query2, (new_event_log_id, bus_id))
  cursor.close()
  connection.close()
  return {"new_eventLog_id": eventlog_id}, 201


def eventLogDelete(id):
  connection = create_connection()
  if connection is None:
                return {"error": "Nie udało się połączyć z bazą danych"}, 500

  cursor = connection.cursor()
  cursor.execute("update bus set actual_event_log_id = null where id = %s", (id,))
  cursor.execute("DELETE FROM event_log WHERE id = %s", (id,))
  connection.commit()
  cursor.close()
  connection.close()
  return {"message": "eventLog został usunięty pomyślnie"}, 200

def eventLogUpdate(id, data):
  if not data:
    return {"error": "Nieprawidłowy format danych JSON"}, 400

  status = data.get('status')
  end_date = data.get('end_date')
  if not all([status, end_date]):
    return {"error": "Brak wymaganych pól"}, 400

  connection = create_connection()
  if connection is None:
    return {"error": "Nie udało się połączyć z bazą danych"}, 500
  cursor = connection.cursor()
  cursor.execute("""
                UPDATE event_log
                SET status = %s, end_date = %s
                WHERE id = %s
            """, (status, end_date, id))
  connection.commit()
  cursor.close()
  connection.close()
  return {"message": "Dane eventu zostały zaktualizowane pomyślnie"}, 200
