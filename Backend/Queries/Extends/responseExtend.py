def concatNameValue(columns, values):
  response = []
  for value in values:
    response_dict = dict(zip(columns, value))
    response.append(response_dict)
  return response