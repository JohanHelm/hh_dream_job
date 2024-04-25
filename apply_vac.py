import requests
from requests import Response
from secrets import resume_id
from tokens import tokens


vacancy = {'id': '97746667', 'premium': False, 'name': 'Программист - разработчик Python', 'department': None,
           'has_test': False, 'response_letter_required': False,
           'area': {'id': '1', 'name': 'Москва', 'url': 'https://api.hh.ru/areas/1'},
           'salary': {'from': 100000, 'to': None, 'currency': 'RUR', 'gross': False},
           'type': {'id': 'open', 'name': 'Открытая'}, 'address': None, 'response_url': None,
           'sort_point_distance': None, 'published_at': '2024-04-23T17:36:47+0300',
           'created_at': '2024-04-23T17:36:47+0300', 'archived': False,
           'apply_alternate_url': 'https://hh.ru/applicant/vacancy_response?vacancyId=97746667',
           'show_logo_in_search': None, 'insider_interview': None,
           'url': 'https://api.hh.ru/vacancies/97746667?host=hh.ru', 'alternate_url': 'https://hh.ru/vacancy/97746667',
           'relations': [], 'employer': {'id': '10937214', 'name': 'Миннегалиев Салих Фаридович',
                                         'url': 'https://api.hh.ru/employers/10937214',
                                         'alternate_url': 'https://hh.ru/employer/10937214', 'logo_urls': {
            'original': 'https://img.hhcdn.ru/employer-logo-original/1258250.jpg',
            '90': 'https://img.hhcdn.ru/employer-logo/6653330.jpeg',
            '240': 'https://img.hhcdn.ru/employer-logo/6653331.jpeg'},
                                         'vacancies_url': 'https://api.hh.ru/vacancies?employer_id=10937214',
                                         'accredited_it_employer': False, 'trusted': False}, 'snippet': {
        'requirement': 'Асинхронное sqlalchemy (asyncpg). Loguru. Уметь работать с базами данных: MariaDB\\MySQL. PostreSQL. Уметь работать с alembic. Уметь работать с VPS...',
        'responsibility': 'Модули:'}, 'contacts': None, 'schedule': {'id': 'remote', 'name': 'Удаленная работа'},
           'working_days': [], 'working_time_intervals': [], 'working_time_modes': [], 'accept_temporary': False,
           'professional_roles': [{'id': '96', 'name': 'Программист, разработчик'}], 'accept_incomplete_resumes': False,
           'experience': {'id': 'between1And3', 'name': 'От 1 года до 3 лет'},
           'employment': {'id': 'full', 'name': 'Полная занятость'}, 'adv_response_url': None, 'is_adv_vacancy': False,
           'adv_context': None}

vacancy_id = vacancy["id"]

url = f"https://api.hh.ru/negotiations"
headers = {"User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.85 Safari/537.36",
           'Authorization': f'Bearer {tokens["access_token"]}'}

params = {"resume_id": resume_id, "vacancy_id": vacancy_id}
response: Response = requests.post(url, headers=headers, data=params)
print(response)
result = response.json()
print(result)
