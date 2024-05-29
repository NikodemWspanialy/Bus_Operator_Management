from database import create_connection
from Queries.Extends.responseExtend import concatNameValue, serializeDate

def combutionGet(id, data):
  connection = create_connection()
  if connection is None:
    return {"error": "Nie udało się połączyć z bazą danych"}, 500
  cursor = connection.cursor()
  query = """select r.date, b.id as bus_id ,SUM(distance) as distance_this_day, re.quantity  from bus b 
            inner join ride r on r.bus_id = b.id
            inner join ride_log rl on rl.ride_id = r.id
            left join refueling re on re.bus_id = b.id
            where r.date = %s
            and re.date = %s
            and b.id = %s
            group by re.quantity, r.date, b.id"""
  cursor.execute(query,(data, data, id))
  columns = [desc[0] for desc in cursor.description]
  data = cursor.fetchall()
  cursor.close()
  connection.close()
  response = concatNameValue(columns, data)
  response = serializeDate(response, 'date')
  return {"combusion:": response}