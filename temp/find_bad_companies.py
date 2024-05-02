from requests import Response, Session
from pathlib import Path
import pickle

from secrets.tokens import tokens
from utils.basic_params import workdir


filename = f"bad_companies.pickle"
fullfilepath = workdir.joinpath(filename)
print(fullfilepath)

if Path.exists(fullfilepath):
    with open(fullfilepath, "rb") as file:
        bad_companies_set = pickle.load(file)

else:
    bad_companies_set = set()

print(len(bad_companies_set))

url = "https://api.hh.ru/vacancies"
headers = {'Authorization': f'Bearer {tokens["access_token"]}'}

search_params = {"page": 0,
                   "per_page": 100,
                   "text": "Центр финансовых технологий",
                   "search_field": "company_name",
                   }

session = Session()
session.headers.update(headers)
session.params = search_params

response: Response = session.get(url)
result = response.json()
vacancies = result["items"]
print(result["found"])

bad_company_names = ('Компьютерная Академия Top',
                     'Компьютерная Академия IT STEP',
                     'Школа программирования JETCODE',
                     'Онлайн-школа Тетрика',
                     'Школа 21',
                     'Компьютерная школа IT-Compot',
                     'Детская школа программирования Софтиум',
                     'ЧУ ДО Московская школа программистов',
                     'Школа программирования Креайтивика',
                     'Школа программирования для детей Code-Class',
                     'Школа программирования Kodland',
                     'Студсервис',
                     'Айтигенио',
                     'ITSTEP Academy Almaty',
                     'Ворк5',
                     'Homework',
                     'EasyCode',
                     'Skyeng',
                     'LATOKEN',
                     'IT школа Hello world',
                     'Хэппи Студент',
                     'ДИСЕНТ',
                     'Таранюк Виталий Геннадьевич',
                     'Nexpanse',
                     'DocuSketch',
                     'JustCode',
                     'Центр финансовых технологий'
                     )

for vacancy in result["items"]:
    print(vacancy['employer'])
    print(vacancy['name'])
    print()
    if vacancy['employer']['name'] in bad_company_names:
        bad_companies_set.add(vacancy['employer']['id'])


print(len(bad_companies_set))

with open(fullfilepath, "wb") as file:
    pickle.dump(bad_companies_set, file)
