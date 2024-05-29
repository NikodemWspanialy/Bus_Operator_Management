from database import create_connection
from Queries.Extends.responseExtend import concatNameValue

def busTypeGetAll():
  connection = create_connection()
  if connection is None:
    return {"error": "Nie udało się połączyć z bazą danych"}, 500
  cursor = connection.cursor()
  query = 'select * from bus_type'
  cursor.execute(query)
  columns = [desc[0] for desc in cursor.description]
  data = cursor.fetchall()
  cursor.close()
  connection.close()
  response = concatNameValue(columns, data)
  return {"busTypes:": response}

def busTypeGetById(id):
  connection = create_connection()
  if connection is None:
    return {"error": "Nie udało się połączyć z bazą danych"}, 500
  cursor = connection.cursor()
  query = 'SELECT * FROM bus_type WHERE id = %s'
  cursor.execute(query, (id,))
  columns = [desc[0] for desc in cursor.description]
  data = cursor.fetchall()
  cursor.close()
  connection.close()
  response = concatNameValue(columns, data)
  return {"bus_type": response}


def busTypeCreate(data):
  description = data.get('description')
  shortcut = data.get('shortcut')
  capacity = data.get('capacity')

  connection = create_connection()
  if connection is None:
    return {"error": "Nie udało się połączyć z bazą danych"}, 500

  cursor = connection.cursor()
  cursor.execute("INSERT INTO bus_type (description, shortcut, capacity) VALUES (%s, %s, %s)", (description, shortcut, capacity))
  connection.commit()

  query = 'SELECT id FROM bus_type where description=%s and shortcut=%s'
  cursor.execute(query,(description, shortcut))
  bustype_id = cursor.fetchall()

  cursor.close()
  connection.close()
  return {"new_bus_type_id": bustype_id}, 201


def busTypeDelete(id):
  connection = create_connection()
  if connection is None:
                return {"error": "Nie udało się połączyć z bazą danych"}, 500

  cursor = connection.cursor()
  cursor.execute("DELETE FROM bus_type WHERE id = %s", (id,))
  connection.commit()
  cursor.close()
  connection.close()
  return {"message": "typ busa został usunięty pomyślnie"}, 200


def busTypeUpdate(data, id):
  if not data:
    return {"error": "Nieprawidłowy format danych JSON"}, 400

  description = data.get('description')
  shortcut = data.get('shortcut')
  capacity = data.get('capacity')

  if not all([description, shortcut, capacity]):
   return {"error": "Brak wymaganych pól"}, 400

  connection = create_connection()
  if connection is None:
    return {"error": "Nie udało się połączyć z bazą danych"}, 500

  cursor = connection.cursor()
  cursor.execute("""UPDATE bus_type SET description = %s, shortcut = %s, capacity = %s WHERE id = %s""", (description, shortcut, capacity, id))
  connection.commit()
  query = 'Select id from bus_type where description = %s and shortcut = %s'
  updated_bus_type_id = cursor.execute(query, (description, shortcut))
  cursor.close()
  connection.close()
  return {"updated_bus_type_id": updated_bus_type_id}, 200