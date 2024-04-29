from pathlib import Path
from datetime import datetime
import pickle
from requests import Response, Session
from secrets.tokens import tokens
from utils.basic_params import workdir


filename = f"applied.pickle"
fullfilepath = workdir.joinpath(filename)
print(fullfilepath)

if Path.exists(fullfilepath):
    with open(fullfilepath, "rb") as file:
        applied_set = pickle.load(file)
else:
    applied_set = set()

print(len(applied_set))

url = "https://api.hh.ru/negotiations"

headers = {"User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.85 Safari/537.36",
           'Authorization': f'Bearer {tokens["access_token"]}'}

params = {"per_page": 100, "page": 11, "order_by":  "created_at"}
session = Session()
session.headers.update(headers)
session.params = params

response: Response = session.get(url)
print(response)
result = response.json()
print(f"found: {result['found']}, pages: {result['pages']}, page: {result['page']}")
# print(*result["items"], sep="\n\n")
for apply in result["items"]:
    create_date = datetime.strptime(apply['created_at'][:-5], '%Y-%m-%dT%H:%M:%S').date()
    if create_date.year == 2024 and apply['resume']['id'] == '15718e69ff0c4be6460039ed1f79366a356e61':
        applied_set.add(apply['vacancy']['id'])

print(len(applied_set))

with open(fullfilepath, "wb") as file:
    pickle.dump(applied_set, file)

# print(applied_set)
