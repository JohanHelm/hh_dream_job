from pathlib import Path
from datetime import datetime
import pickle
from requests import Response, Session
from secrets.tokens import tokens
from secrets.client_secrets import resume_id
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

headers = {'Authorization': f'Bearer {tokens["access_token"]}'}

session = Session()
session.headers.update(headers)
params = {"per_page": 100, "page": 100, "order_by":  "created_at"} # почему то не возвращает результаты для страниц > 100
# session.params = params
# response: Response = session.get(url)
# result = response.json()
# print(result)
# print(f"found: {result['found']}, pages: {result['pages']}, page: {result['page']}")

for page in range(101):
    params = {"per_page": 100, "page": page, "order_by":  "created_at"}
    session.params = params

    response: Response = session.get(url)
    print(response)
    result = response.json()
    print(f"found: {result['found']}, pages: {result['pages']}, page: {result['page']}")

    for apply in result["items"]:
        create_date = datetime.strptime(apply['created_at'][:-5], '%Y-%m-%dT%H:%M:%S').date()
        if create_date.year in (2024, 2025) and apply['resume']['id'] == resume_id:
            applied_set.add(apply['vacancy']['id'])

    print(len(applied_set))

with open(fullfilepath, "wb") as file:
    pickle.dump(applied_set, file)
