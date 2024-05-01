from requests import Response, Session

from secrets.tokens import tokens

vacancy_id = 97090543

url = f"https://api.hh.ru/vacancies/favorited/{vacancy_id}"
headers = {'Authorization': f'Bearer {tokens["access_token"]}'}

session = Session()
session.headers.update(headers)
response: Response = session.request("PUT", url, allow_redirects=False)
print(response)
print(response.text)
