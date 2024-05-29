from database import create_connection
from Queries.Extends.responseExtend import concatNameValue, serializeDate

def driverCombutionGet(id, data):
  connection = create_connection()
  if connection is None:
    return {"error": "Nie udało się połączyć z bazą danych"}, 500
  cursor = connection.cursor()
  query = """select d.id as driver_id, d.name, d.lastname, r.date, SUM(distance) as distance, quantity from driver d
inner join ride r on d.id = r.driver_id
inner join ride_log rl on rl.ride_id = r.id
inner join bus b on b.id = r.bus_id
inner join refueling re on re.bus_id = b.id
where d.id = %s
and r.date = %s
and re.date = %s
group by d.id, d.name, d.lastname, r.date, quantity"""
  cursor.execute(query,(id, data, data))
  columns = [desc[0] for desc in cursor.description]
  data = cursor.fetchall()
  cursor.close()
  connection.close()
  response = concatNameValue(columns, data)
  response = serializeDate(response, 'date')
  return {"combusion:": response}