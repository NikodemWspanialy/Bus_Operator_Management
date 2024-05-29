def concatNameValue(columns, values):
  response = []
  for value in values:
    response_dict = dict(zip(columns, value))
    response.append(response_dict)
  return response


def serializeDataTime(collection, name):
  for obj in collection:
    obj[name] = obj[name].strftime('%H:%M:%S')
  return collection

def serializeDate(collection, name):
    for obj in collection:
        obj[name] = obj[name].strftime('%Y-%m-%d')
    return collection