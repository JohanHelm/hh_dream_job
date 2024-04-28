from requests import Response, Session

from secrets.client_secrets import resume_id
from secrets.tokens import tokens

# vacancy = {'id': '95616891', 'premium': False, 'name': 'Разработчик/аналитик Python/SQL', 'department': None,
#            'has_test': False, 'response_letter_required': False,
#            'area': {'id': '1', 'name': 'Москва', 'url': 'https://api.hh.ru/areas/1'},
#            'salary': {'from': 100000, 'to': None, 'currency': 'RUR', 'gross': False},
#            'type': {'id': 'open', 'name': 'Открытая'},
#            'address': {'city': 'Москва', 'street': 'Нижняя Красносельская улица', 'building': '40/12к20',
#                        'lat': 55.773854, 'lng': 37.671462, 'description': None,
#                        'raw': 'Москва, Нижняя Красносельская улица, 40/12к20',
#                        'metro': {'station_name': 'Бауманская', 'line_name': 'Арбатско-Покровская', 'station_id': '3.17',
#                                  'line_id': '3', 'lat': 55.772405, 'lng': 37.67904}, 'metro_stations': [
#                    {'station_name': 'Бауманская', 'line_name': 'Арбатско-Покровская', 'station_id': '3.17',
#                     'line_id': '3', 'lat': 55.772405, 'lng': 37.67904},
#                    {'station_name': 'Красносельская', 'line_name': 'Сокольническая', 'station_id': '1.60',
#                     'line_id': '1', 'lat': 55.780014, 'lng': 37.666097}], 'id': '14806716'}, 'response_url': None,
#            'sort_point_distance': None, 'published_at': '2024-03-27T13:30:27+0300',
#            'created_at': '2024-03-27T13:30:27+0300', 'archived': False,
#            'apply_alternate_url': 'https://hh.ru/applicant/vacancy_response?vacancyId=95616891',
#            'show_logo_in_search': None, 'insider_interview': None,
#            'url': 'https://api.hh.ru/vacancies/95616891?host=hh.ru', 'alternate_url': 'https://hh.ru/vacancy/95616891',
#            'relations': [],
#            'employer': {'id': '2161785', 'name': 'Digital Strategy', 'url': 'https://api.hh.ru/employers/2161785',
#                         'alternate_url': 'https://hh.ru/employer/2161785',
#                         'logo_urls': {'90': 'https://img.hhcdn.ru/employer-logo/5986001.png',
#                                       '240': 'https://img.hhcdn.ru/employer-logo/5986002.png',
#                                       'original': 'https://img.hhcdn.ru/employer-logo-original/1091345.png'},
#                         'vacancies_url': 'https://api.hh.ru/vacancies?employer_id=2161785',
#                         'accredited_it_employer': False, 'trusted': True}, 'snippet': {
#         'requirement': 'Понимание принципов архитектуры баз и хранилищ данных. —Знание библиотек <highlighttext>Python</highlighttext>, необходимых для работы с данными (numpy, pandas) и создания витрин...',
#         'responsibility': 'Автоматизация сбора и агрегации данных, реализация дашбордов для мониторинга KPI, управления рекламными кампаниями и каналами продаж. — Поддержка и развития внутренней...'},
#            'contacts': {'name': 'Иванова Элина', 'email': 'elina.ivanova@ds.team', 'phones': [
#                {'comment': None, 'city': '966', 'number': '2618616', 'country': '7', 'formatted': '+79662618616'}],
#                         'call_tracking_enabled': True}, 'schedule': {'id': 'remote', 'name': 'Удаленная работа'},
#            'working_days': [], 'working_time_intervals': [], 'working_time_modes': [], 'accept_temporary': False,
#            'professional_roles': [{'id': '10', 'name': 'Аналитик'}], 'accept_incomplete_resumes': False,
#            'experience': {'id': 'between1And3', 'name': 'От 1 года до 3 лет'},
#            'employment': {'id': 'full', 'name': 'Полная занятость'}, 'adv_response_url': None, 'is_adv_vacancy': False,
#            'adv_context': None}

# vacancy_id = vacancy["id"]
vacancy_id = 91947354

url = f"https://api.hh.ru/negotiations"
headers = {
    # "User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.85 Safari/537.36",
    'Authorization': f'Bearer {tokens["access_token"]}'}

data = {"resume_id": resume_id, "vacancy_id": vacancy_id}
# response: Response = requests.post(url, headers=headers, data=params)

session = Session()
session.headers.update(headers)
# session.params = data
response: Response = session.request("POST", url, params=data, allow_redirects=False)
print(response)
print(response.text)
# result = response.json()
# print(result)
