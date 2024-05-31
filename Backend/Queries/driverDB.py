from database import create_connection
from Queries.Extends.responseExtend import concatNameValue

def driverGetAll():
  connection = create_connection()
  if connection is None:
    return {"error": "Nie udało się połączyć z bazą danych"}, 500
  cursor = connection.cursor()
  query = 'SELECT * FROM public."driver"'
  cursor.execute(query)
  columns = [desc[0] for desc in cursor.description]
  drivers = cursor.fetchall()
  cursor.close()
  connection.close()
  response = concatNameValue(columns, drivers)
  return {"drivers": response}

def driverGetById(id):
  connection = create_connection()
  if connection is None:
                return {"error": "Nie udało się połączyć z bazą danych"}, 500

  cursor = connection.cursor()
  query = 'SELECT * FROM driver WHERE id = %s'
  cursor.execute(query, (id,))
  columns = [desc[0] for desc in cursor.description]
  driver = cursor.fetchall()
  cursor.close()
  connection.close()
  response = concatNameValue(columns, driver)
  return {"driver": response}


def driverCreate(data):
  name = data.get('name')
  lastname = data.get('lastname')
  license = data.get('license')
  salary = data.get('salary')
  holidays_days = data.get('holidays_days')

  connection = create_connection()
  if connection is None:
    return {"error": "Nie udało się połączyć z bazą danych"}, 500

  cursor = connection.cursor()
  cursor.execute("INSERT INTO driver (name, lastname, license, salary, holidays_days) VALUES (%s, %s, %s, %s, %s)", (name, lastname, license, salary, holidays_days))
  connection.commit()

  query = 'SELECT id FROM driver where name=%s and lastname=%s'
  cursor.execute(query,(name, lastname))
  driver_id = cursor.fetchall()

  cursor.close()
  connection.close()
  return {"new_driver_id": driver_id}, 201


def driverDelete(id):
  connection = create_connection()
  if connection is None:
                return {"error": "Nie udało się połączyć z bazą danych"}, 500

  cursor = connection.cursor()
  cursor.execute("DELETE FROM driver WHERE id = %s", (id,))
  connection.commit()
  cursor.close()
  connection.close()
  return {"message": "Kierowca został usunięty pomyślnie"}, 200


def driverUpdate(data, id):
  if not data:
    return {"error": "Nieprawidłowy format danych JSON"}, 400

  name = data.get('name')
  lastname = data.get('lastname')
  license = data.get('license')
  salary = data.get('salary')
  holidays_days = data.get('holidays_days')

  if not all([name, lastname, license]):
   return {"error": "Brak wymaganych pól"}, 400

  connection = create_connection()
  if connection is None:
    return {"error": "Nie udało się połączyć z bazą danych"}, 500

  cursor = connection.cursor()
  cursor.execute("""
    UPDATE driver
    SET name = %s, lastname = %s, license = %s, salary = %s, holidays_days = %s
    WHERE id = %s
    """, (name, lastname, license, salary, holidays_days, id))
  connection.commit()
  cursor.close()
  connection.close()
  return {"updated_driver_id": id}, 200