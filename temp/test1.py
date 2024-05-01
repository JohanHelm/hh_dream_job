from api_requests.api_querry import ApiClient
from operations.vacancy_handler import ApplicantManager
from secrets.tokens import tokens
from utils.basic_params import basic_url
from operations.applicant_params import applicant_params


api_client = ApiClient()
vacancy_manager = ApplicantManager(api_client)
vacancy_manager.search_vacancy(applicant_params[4])
vacancy_manager.remove_already_applied()
vacancy_manager.remove_bad_companies()
len_before_add = len(vacancy_manager.vacancy_list)
print(len_before_add)
len_vacancy_to_add = len(list(filter(lambda x: x["has_test"], vacancy_manager.vacancy_list)))
print(len_vacancy_to_add)
vacancy_manager.add_to_favorite_with_test()
print()
assert len(create_vacancy_manager.vacancy_list) == len_before_add - len_vacancy_to_add

