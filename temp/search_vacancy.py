from requests import Response, Session
from secrets.client_secrets import resume_id
from secrets.tokens import tokens
from operations.applicant_params import *



# url = f"https://api.hh.ru/resumes/{resume_id}/similar_vacancies"
url = "https://api.hh.ru/vacancies"
headers = {
    # "User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.85 Safari/537.36",
    'Authorization': f'Bearer {tokens["access_token"]}',
}

session = Session()
# print(session.__dict__)
session.headers.update(headers)
# print(session.__dict__)
session.params = search_params_4
# print(session.__dict__)
# session.__delattr__("params")
# print(session.__dict__)


response: Response = session.get(url)
result = response.json()
vacancies = result["items"]
print(result["found"])
del result['items']
print(result)
# print(*result["items"], sep="\n\n")


