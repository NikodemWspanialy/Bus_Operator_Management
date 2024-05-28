from database import create_connection
from Queries.Extends.responseExtend import concatNameValue

def routeGetByLineId(id):
  connection = create_connection()
  if connection is None:
    return {"error": "Nie udało się połączyć z bazą danych"}, 500
  cursor = connection.cursor()
  query = 'select r.id, bs.id, bs.name, r.order from route r inner join bus_stop bs on bs.id = r.bus_stop_id where r.line_id = %s order by r.order'
  cursor.execute(query, (id,))
  routes = cursor.fetchall()
  columns = [desc[0] for desc in cursor.description]
  cursor.close()
  connection.close()
  response = concatNameValue(columns, routes);         
  return {"routes": response}