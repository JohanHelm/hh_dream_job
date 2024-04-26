import pickle
from requests import Response
from loguru import logger

from api_requests.api_query import ApiClient
from basic_params import search_params
from secrets.client_secrets import resume_id


class VacancyManager:
    def __init__(self, api_client):
        self.apply_counter: int = 0
        self.apply_limit: int = 195
        self.apply_limit: int = 5
        self.api_client: ApiClient = api_client
        self.vacancy_list: list[dict] = []

    def search_similar_vacancy(self):
        self.api_client.set_session_params(search_params)
        url = f"https://api.hh.ru/resumes/{resume_id}/similar_vacancies"
        response: Response = self.api_client.safe_querry("GET", url)
        if response.status_code == 200:
            result = response.json()
            logger.info(f"found by similar search {result['found']} vacancies")
            self.vacancy_list = result["items"]
        elif response.status_code in (400, 404):
            logger.warning(f"failure to search_similar_vacancy with response {response}")
            with open('search_similar_vacancy_errors.json', 'w') as file:
                file.write(response.json())
        else:
            logger.warning(f"failure to search_similar_vacancy with response {response}")

    def remove_has_test(self):
        self.vacancy_list = list(filter(lambda x: not x["has_test"], self.vacancy_list))
        logger.info(f"without test we got {len(self.vacancy_list)} vacancies")

    def pickle_vacancies(self):
        with open("vacancies.pickle", "wb") as file:
            pickle.dump(self.vacancy_list, file)
            logger.info(f"save binary file vacancies.pickle")

    def unpickle_vacancies(self):
        with open("vacancies.pickle", "rb") as file:
            logger.info(f"open binary file vacancies.pickle")
            self.vacancy_list = pickle.load(file)

    def appy_without_letter(self):
        url = f"https://api.hh.ru/negotiations"
        params = {"resume_id": resume_id}
        self.api_client.set_session_params(params)
        vacancies_to_apply = filter(lambda x: not x["response_letter_required"], self.vacancy_list)
        for vacancy in vacancies_to_apply:
            self.api_client.session.params["vacancy_id"] = vacancy["id"]
            response: Response = self.api_client.safe_querry("POST", url)
            if response.status_code == 201:
                self.apply_counter += 1
                if self.apply_counter == self.apply_limit:
                    logger.info(f"exceed apply limit for today")
                    break
            elif response.status_code in (400, 403, 303):
                logger.warning(f"failure to appy_without_letter vacancy with response {response}")
                with open('appy_without_letter_errors.json', 'w') as file:
                    file.write(response.json())
            else:
                logger.warning(f"failure to appy_without_letter with response {response}")
        logger.info(f"total appy_without_letter is {self.apply_counter}")


        # print(*vacancies_to_apply, sep="\n\n")





    def apply_with_letter(self):
        pass



