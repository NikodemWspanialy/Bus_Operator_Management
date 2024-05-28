from database import create_connection
from Queries.Extends.responseExtend import concatNameValue, serializeDataTime

def busStopScheduleGetAllByBusStopId(id):
  connection = create_connection()
  if connection is None:
    return {"error": "Nie udało się połączyć z bazą danych"}, 500
  cursor = connection.cursor()
  query = 'select tr.id, l.line_name, tr.time from trackroute tr inner join route r on tr.route_id = r.id inner join line l on l.id = r.line_id where r.bus_stop_id = %s order by r.line_id, time'
  cursor.execute(query,(id,))
  departures = cursor.fetchall()
  columns = [desc[0] for desc in cursor.description]
  cursor.close()
  connection.close()
  response = concatNameValue(columns, departures)
  response = serializeDataTime(response, 'time')
  return {"departures": response}