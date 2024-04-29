from requests import Response, Session

from secrets.client_secrets import resume_id
from secrets.tokens import tokens

vacancy_id = 97090543

url = f"https://api.hh.ru/vacancies/favorited/{vacancy_id}"
headers = {
    # "User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.85 Safari/537.36",
    'Authorization': f'Bearer {tokens["access_token"]}'}

# data = {"resume_id": resume_id, "vacancy_id": vacancy_id}
# response: Response = requests.post(url, headers=headers, data=params)

session = Session()
session.headers.update(headers)
# session.params = data
response: Response = session.request("PUT", url, allow_redirects=False)
print(response)
print(response.text)

# print(response.json())
