from pathlib import Path
from datetime import datetime
import pickle
from requests import Response, Session
from secrets.tokens import tokens




# url = "https://api.hh.ru/areas"
url = "https://api.hh.ru/dictionaries"
# url = "https://api.hh.ru/professional_roles"
# url = "https://api.hh.ru/negotiations"

headers = {'Authorization': f'Bearer {tokens["access_token"]}'}

params = {"per_page": 100, "page": 8, "order_by":  "created_at"}
session = Session()
session.headers.update(headers)
session.params = params

response: Response = session.get(url)
print(response)
result = response.json()
print(result["vacancy_search_fields"])

