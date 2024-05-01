from requests import Response, Session

from secrets.client_secrets import resume_id
from secrets.tokens import tokens

vacancy_id = 97618793

url = f"https://api.hh.ru/negotiations"
headers = {'Authorization': f'Bearer {tokens["access_token"]}'}

params = {"resume_id": resume_id, "vacancy_id": vacancy_id}


session = Session()
session.headers.update(headers)
response: Response = session.request("POST", url, params=params, allow_redirects=False)
print(response)
print(response.headers)
