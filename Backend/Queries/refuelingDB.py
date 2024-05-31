from database import create_connection
from Queries.Extends.responseExtend import concatNameValue, serializeDate


def refuelingGetAll():
  connection = create_connection()
  if connection is None:
    return {"error": "Nie udało się połączyć z bazą danych"}, 500
  cursor = connection.cursor()
  query = 'select * from refueling'
  cursor.execute(query)
  refueling = cursor.fetchall()
  columns = [desc[0] for desc in cursor.description]
  cursor.close()
  connection.close()
  response = concatNameValue(columns, refueling)
  response = serializeDate(response, 'date')
  return {"buses": response}

def refuelingGetByBusId(id):
  connection = create_connection()
  if connection is None:
    return {"error": "Nie udało się połączyć z bazą danych"}, 500
  cursor = connection.cursor()
  query = 'select * from refueling where bus_id = %s'
  cursor.execute(query,(id,))
  refueling = cursor.fetchall()
  columns = [desc[0] for desc in cursor.description]
  cursor.close()
  connection.close()
  response = concatNameValue(columns, refueling)
  response = serializeDate(response, 'date')
  return {"buses": response}

def refuelingGetByDate(date):
  connection = create_connection()
  if connection is None:
    return {"error": "Nie udało się połączyć z bazą danych"}, 500
  cursor = connection.cursor()
  query = 'select * from refueling where date = %s'
  cursor.execute(query,(date,))
  refueling = cursor.fetchall()
  columns = [desc[0] for desc in cursor.description]
  cursor.close()
  connection.close()
  response = concatNameValue(columns, refueling)
  response = serializeDate(response, 'date')
  return {"buses": response}

def refuelingCreate(data):
  connection = create_connection()
  if connection is None:
    return {"error": "Nie udało się połączyć z bazą danych"}, 500
  cursor = connection.cursor()
  bus_id = data.get('bus_id')
  quantity = data.get('quantity')
  date = data.get('date')

  cursor.execute("INSERT INTO refueling (bus_id, quantity, date) VALUES (%s, %s, %s)", (bus_id, quantity, date))
  connection.commit()
  cursor.close()
  connection.close()
  return {"message": "Nowy refueling został dodany pomyślnie"}, 201