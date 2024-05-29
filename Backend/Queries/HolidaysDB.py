from database import create_connection
from Queries.Extends.responseExtend import concatNameValue, serializeDate

#CRUD caly

def holidaysGetAll():
  connection = create_connection()
  if connection is None:
                return {"error": "Nie udało się połączyć z bazą danych"}, 500

  cursor = connection.cursor()
  query = 'select * from driver_unavailability'
  cursor.execute(query)
  columns = [desc[0] for desc in cursor.description]
  holidays = cursor.fetchall()
  cursor.close()
  connection.close()
  response = concatNameValue(columns, holidays)
  response = serializeDate(response, 'start_date')
  response = serializeDate(response, 'end_date')
  return {"holidays": holidays}

def holidaysGetByDriverId(id):
  connection = create_connection()
  if connection is None:
                return {"error": "Nie udało się połączyć z bazą danych"}, 500
  cursor = connection.cursor()
  query = 'select * from driver_unavailability where driver_id = %s'
  cursor.execute(query, (id,))
  columns = [desc[0] for desc in cursor.description]
  holidays = cursor.fetchall()
  cursor.close()
  connection.close()
  response = concatNameValue(columns, holidays)
  response = serializeDate(response, 'start_date')
  response = serializeDate(response, 'end_date')
  return {"holidays": holidays}

def holidaysCreate(data):
  connection = create_connection()
  if connection is None:
    return {"error": "Nie udało się połączyć z bazą danych"}, 500
  cursor = connection.cursor()
  driver_id = data.get('driver_id')
  start_date = data.get('start_date')
  end_date = data.get('end_date')
  reason = data.get('reason')
  cursor.execute("INSERT INTO driver_unavailability (driver_id, start_date, end_date, reason) VALUES (%s, %s, %s, %s)", (driver_id, start_date, end_date, reason))
  connection.commit()
  cursor.close()
  connection.close()
  return {"message": "Nowy urlop został dodany pomyślnie"}, 201

def holidaysDelete(id):
  return {"message": "Nie zaimplementonane - Nikodem i pewnie nie bedzie ten endpoint bo by wszystkie usunelo od danego kierowcy"}, 201

def holidaysUpdate(data):
  return {"message": "Nie zaimplementonane - Nikodem i pewnie nie bedzie ten endpoint bo by wszystkie usunelo od danego kierowcy"}, 201