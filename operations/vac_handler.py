from requests import Response
from loguru import logger

from api_requests.api_query import ApiClient
from basic_params import search_params
from secrets.client_secrets import resume_id


class VacancyManager:
    def __init__(self, api_client):
        self.apply_counter: int = 0
        self.api_client: ApiClient = api_client
        self.vacancy_list = []

    def search_similar_vacancy(self):
        self.api_client.set_session_params(search_params)
        url = f"https://api.hh.ru/resumes/{resume_id}/similar_vacancies"
        response: Response = self.api_client.safe_get("GET", url)
        if response == 200:
            result = response.json()
            self.vacancy_list = result["items"]

        else:
            logger.warning(f"failure to search_similar_vacancy")
            with open('search_similar_vacancy_errors.json', 'w') as file:
                file.write(response.json())
