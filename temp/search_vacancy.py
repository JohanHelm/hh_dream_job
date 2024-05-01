from requests import Response, Session

from secrets.tokens import tokens
from operations.applicant_params import *



url = f"https://api.hh.ru/resumes/{resume_id}/similar_vacancies"
# url = "https://api.hh.ru/vacancies"

headers = {'Authorization': f'Bearer {tokens["access_token"]}'}

session = Session()
session.headers.update(headers)
session.params = search_params_2

response: Response = session.get(url)
result = response.json()
vacancies = result["items"]
print(result["found"])

for vacancy in result["items"]:
    print(vacancy['name'])
    print(vacancy['area'])
    print(vacancy['employer'])
    print(vacancy['snippet'])
    print(vacancy['professional_roles'])
    print()

del result['items']
print(result)



