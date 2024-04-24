import requests
from requests import Response, Session
from secrets import resume_id
from tokens import tokens
from search_params import SearchParams

url = f"https://api.hh.ru/resumes/{resume_id}/similar_vacancies"
headers = {"User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.85 Safari/537.36",
           'Authorization': f'Bearer {tokens["access_token"]}'}

session = Session()
session.headers.update(headers)
search_params = SearchParams().__dict__
session.params = search_params

response: Response = session.get(url)
result = response.json()
vacancies = result["items"]
print(result["found"])
print(*result["items"][0])


