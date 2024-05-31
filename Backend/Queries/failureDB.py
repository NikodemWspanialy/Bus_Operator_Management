from database import create_connection
from Queries.Extends.responseExtend import concatNameValue, serializeDate

def failureGet(data):
  connection = create_connection()
  if connection is None:
    return {"error": "Nie udało się połączyć z bazą danych"}, 500
  cursor = connection.cursor()
  query = """select b.id as bus_id, date, ride_id, accident  from bus b
inner join ride r on b.id = r.bus_id
inner join ride_log rl on r.id = rl.ride_id
and date = %s
and accident <> '' 
"""
  cursor.execute(query,(data, ))
  columns = [desc[0] for desc in cursor.description]
  data = cursor.fetchall()
  cursor.close()
  connection.close()
  response = concatNameValue(columns, data)
  response = serializeDate(response, 'date')
  return {"combusion:": response}

def failureGetById(id, data):
  connection = create_connection()
  if connection is None:
    return {"error": "Nie udało się połączyć z bazą danych"}, 500
  cursor = connection.cursor()
  query = """select b.id as bus_id, date, ride_id, accident  from bus b
inner join ride r on b.id = r.bus_id
inner join ride_log rl on r.id = rl.ride_id
where b.id = %s
and date = %s
and accident <> '' 
"""
  cursor.execute(query,(id, data))
  columns = [desc[0] for desc in cursor.description]
  data = cursor.fetchall()
  cursor.close()
  connection.close()
  response = concatNameValue(columns, data)
  response = serializeDate(response, 'date')
  return {"combusion:": response}
def failureGetAll(data):
  connection = create_connection()
  if connection is None:
    return {"error": "Nie udało się połączyć z bazą danych"}, 500
  cursor = connection.cursor()
  query = """select b.id as bus_id, date, ride_id, accident  from bus b
inner join ride r on b.id = r.bus_id
inner join ride_log rl on r.id = rl.ride_id
and date = %s"""
  cursor.execute(query,(data,))
  columns = [desc[0] for desc in cursor.description]
  data = cursor.fetchall()
  cursor.close()
  connection.close()
  response = concatNameValue(columns, data)
  response = serializeDate(response, 'date')
  return {"combusion:": response}

def failureGetAllById(id, data):
  connection = create_connection()
  if connection is None:
    return {"error": "Nie udało się połączyć z bazą danych"}, 500
  cursor = connection.cursor()
  query = """select b.id as bus_id, date, ride_id, accident  from bus b
inner join ride r on b.id = r.bus_id
inner join ride_log rl on r.id = rl.ride_id
where b.id = %s
and date = %s
"""
  cursor.execute(query,(id, data))
  columns = [desc[0] for desc in cursor.description]
  data = cursor.fetchall()
  cursor.close()
  connection.close()
  response = concatNameValue(columns, data)
  response = serializeDate(response, 'date')
  return {"combusion:": response}