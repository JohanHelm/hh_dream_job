from api_requests.api_querry import ApiClient
from operations.vacancy_handler import ApplicantManager
from secrets.tokens import tokens
from utils.basic_params import basic_url

api_client = ApiClient()
vacancy_manager = ApplicantManager(api_client)
attributes = vacancy_manager.__dict__

print(attributes)
attributes = {'url_for_apply': f'{basic_url}/negotiations',
              'search_step': 0,
              'pages_found': 1,
              'apply_counter': 0,
              'apply_limit': 195,
              'api_client': api_client,
              'vacancy_list': [],
              'applied_set': set(),
              'bad_companies': set()}

assert vacancy_manager.__dict__ == attributes

