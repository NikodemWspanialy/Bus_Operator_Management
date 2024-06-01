from database import create_connection
from Queries.Extends.responseExtend import concatNameValue

def lineGetAll():
  connection = create_connection()
  if connection is None:
    return {"error": "Nie udało się połączyć z bazą danych"}, 500
  cursor = connection.cursor()
  query = """select id, line_name as name from line
  """
  cursor.execute(query)
  columns = [desc[0] for desc in cursor.description]
  lines = cursor.fetchall()
  cursor.close()
  connection.close()
  response = concatNameValue(columns, lines)
  return {"lines": response}

def lineGetById(id):
  connection = create_connection()
  if connection is None:
                return {"error": "Nie udało się połączyć z bazą danych"}, 500

  cursor = connection.cursor()
  query = """select id, line_name as name from line where id = %s"""
  cursor.execute(query, (id,))
  columns = [desc[0] for desc in cursor.description]
  rides = cursor.fetchall()
  cursor.close()
  connection.close()
  response = concatNameValue(columns, rides)
  return {"line": response}

def lineGetByName(name):
  connection = create_connection()
  if connection is None:
                return {"error": "Nie udało się połączyć z bazą danych"}, 500

  cursor = connection.cursor()
  query = """select id, line_name as name from line where line_name = %s"""
  cursor.execute(query, (name,))
  columns = [desc[0] for desc in cursor.description]
  rides = cursor.fetchall()
  cursor.close()
  connection.close()
  response = concatNameValue(columns, rides)
  return {"line": response}

def lineCreate(name):

  connection = create_connection()
  if connection is None:
    return {"error": "Nie udało się połączyć z bazą danych"}, 500

  cursor = connection.cursor()
  query = """INSERT INTO line (line_name)
  VALUES (%s)"""
  cursor.execute(query, (name,))
  connection.commit()

  query = """select id from line where line_name = %s"""
  cursor.execute(query,(name,))
  ride_id = cursor.fetchall()

  cursor.close()
  connection.close()
  return {"new_line_id": ride_id}, 201


def lineDelete(id):
  connection = create_connection()
  if connection is None:
                return {"error": "Nie udało się połączyć z bazą danych"}, 500

  cursor = connection.cursor()
  cursor.execute("DELETE FROM line WHERE id = %s", (id,))
  connection.commit()
  cursor.close()
  connection.close()
  return {"message": "linia został usunięty pomyślnie"}, 200


def lineUpdate(id, name):
  connection = create_connection()
  if connection is None:
    return {"error": "Nie udało się połączyć z bazą danych"}, 500

  cursor = connection.cursor()
  cursor.execute("""
    UPDATE line set line_name = %s
where id = %s 
    """, (name, id))
  connection.commit()
  cursor.close()
  connection.close()
  return {"updated_line_id": id}, 200