import json
import pickle
from requests import Response
from loguru import logger
from datetime import datetime

from api_requests.api_query import ApiClient
from basic_params import search_params, basic_url, create_response_letter
from secrets.client_secrets import resume_id
from database import Database


class VacancyManager:
    def __init__(self, api_client):
        self.url_for_apply = f"{basic_url}/negotiations"
        self.url_for_similar_search = f"{basic_url}/resumes/{resume_id}/similar_vacancies"
        self.url_for_common_search = f"{basic_url}/vacancies"
        self.search_iteration: int = 1
        self.apply_counter: int = 0
        self.apply_limit: int = 195
        self.api_client: ApiClient = api_client
        self.vacancy_list: list[dict] = []
        self.db = Database("dream_job.db")

    def search_similar_vacancy(self):
        self.api_client.set_session_params(search_params)
        response: Response = self.api_client.safe_querry("GET", self.url_for_similar_search)
        if response.status_code == 200:
            result = response.json()
            logger.info(f"found by similar search {result['found']} vacancies")
            self.vacancy_list = result["items"]
        elif response.status_code in (400, 404):
            logger.warning(f"failure to search_similar_vacancy with response {response}")
            with open('search_similar_vacancy_errors.json', 'w') as file:
                file.write(str(datetime.utcnow()))
                json.dump(response.json(), file, separators=(',\n', ': '))
                file.write("\n\n")
        else:
            logger.warning(f"failure to search_similar_vacancy with response {response}")

    def search_common_vacancy(self):
        self.api_client.set_session_params(search_params)
        response: Response = self.api_client.safe_querry("GET", self.url_for_common_search)
        if response.status_code == 200:
            result = response.json()
            logger.info(f"found by common search {result['found']} vacancies")
            self.vacancy_list = result["items"]
        elif response.status_code in (400, 404):
            logger.warning(f"failure to search_common_vacancy with response {response}")
            with open('search_common_vacancy_errors.json', 'w') as file:
                file.write(str(datetime.utcnow()))
                json.dump(response.json(), file, separators=(',\n', ': '))
                file.write("\n\n")
        else:
            logger.warning(f"failure to search_common_vacancy with response {response}")

    def remove_has_test(self):
        self.vacancy_list = list(filter(lambda x: not x["has_test"], self.vacancy_list))
        logger.info(f"without test we got {len(self.vacancy_list)} vacancies")

    def remove_already_applied(self):
        already_applied = [item[0] for item in self.db.get_already_applied()]
        self.vacancy_list = list(filter(lambda x: int(x["id"]) not in already_applied, self.vacancy_list))
        logger.info(f"we got {len(self.vacancy_list)} not applied vacancies yet")

    def pickle_vacancies(self):
        with open("vacancies.pickle", "wb") as file:
            pickle.dump(self.vacancy_list, file)
            logger.info(f"save binary file vacancies.pickle")

    def unpickle_vacancies(self):
        with open("vacancies.pickle", "rb") as file:
            logger.info(f"open binary file vacancies.pickle")
            self.vacancy_list = pickle.load(file)

    def apply_without_letter(self):
        params = {"resume_id": resume_id}
        self.api_client.set_session_params(params)
        vacancies_to_apply = filter(lambda x: not x["response_letter_required"], self.vacancy_list)
        for vacancy in vacancies_to_apply:
            self.api_client.session.params["vacancy_id"] = vacancy["id"]
            response: Response = self.api_client.safe_querry("POST", self.url_for_apply)
            if response.status_code == 201:
                self.apply_counter += 1
                self.db.add_vacancy_id(vacancy["id"])
                if self.apply_counter == self.apply_limit:
                    logger.info(f"exceed apply limit for today")
                    break
            elif response.status_code in (400, 403, 303):
                logger.warning(f"failure to appy_without_letter vacancy {vacancy['id']} with response {response}")
                with open('appy_without_letter_errors.json', 'w') as file:
                    file.write(str(datetime.utcnow()))
                    file.write(vacancy["id"])
                    json.dump(response.json(), file, separators=(',\n', ': '))
                    file.write("\n\n")
            else:
                logger.warning(f"failure to appy_without_letter vacancy {vacancy['id']} with response {response}")
        logger.info(f"total appy_without_letter is {self.apply_counter}")

    def apply_with_letter(self):
        params = {"resume_id": resume_id}
        self.api_client.set_session_params(params)
        vacancies_to_apply = filter(lambda x: x["response_letter_required"], self.vacancy_list)
        for vacancy in vacancies_to_apply:
            self.api_client.session.params["vacancy_id"] = vacancy["id"]
            self.api_client.session.params["message"] = create_response_letter(vacancy_url=vacancy["alternate_url"],
                                                                               vacancy_name=vacancy["name"])
            response: Response = self.api_client.safe_querry("POST", self.url_for_apply)
            if response.status_code == 201:
                self.apply_counter += 1
                self.db.add_vacancy_id(vacancy["id"])
                if self.apply_counter == self.apply_limit:
                    logger.info(f"exceed apply limit for today")
                    break
            elif response.status_code in (400, 403, 303):
                logger.warning(f"failure to appy_with_letter vacancy {vacancy['id']} with response {response}")
                with open('appy_with_letter_errors.json', 'a') as file:
                    file.write(str(datetime.utcnow()))
                    file.write(vacancy["id"])
                    json.dump(response.json(), file, separators=(',\n', ': '))
                    file.write("\n\n")
            else:
                logger.warning(f"failure to appy_with_letter vacancy {vacancy['id']} with response {response}")
        logger.info(f"total appy_with_letter is {self.apply_counter}")


