import json
import pickle
from pathlib import Path
from requests import Response
from loguru import logger
from datetime import datetime

from api_requests.api_query import ApiClient
from utils.basic_params import basic_url, create_response_letter, workdir
from secrets.client_secrets import resume_id
from applicant_params import applicant_params, Params


class ApplicantManager:
    def __init__(self, api_client):
        self.url_for_apply = f"{basic_url}/negotiations"
        self.search_iteration: int = 0
        self.pages_found: int | None = None
        self.apply_counter: int = 0
        self.apply_limit: int = 195
        self.api_client: ApiClient = api_client
        self.vacancy_list: list[dict] = []
        self.applied_set: set[str] = set()
        self.unpickle_applied()

    def search_vacancy(self, params: Params):
        self.api_client.set_session_params(params.search_params)
        response: Response = self.api_client.safe_querry("GET", params.search_url)
        if response.status_code == 200:
            result = response.json()
            logger.info(f"found by {params.search_mode} search {result['found']} vacancies")
            self.pages_found = result["pages"]
            self.vacancy_list = result["items"]
        elif response.status_code in (400, 404):
            logger.warning(f"failure to search in {params.search_mode} with response {response}")
            with open(f'search_{params.search_mode}_vacancy_errors.json', 'w') as file:
                file.write(str(datetime.utcnow()))
                json.dump(response.json(), file, separators=(',\n', ': '))
                file.write("\n\n")
        else:
            logger.warning(f"failure to search in {params.search_mode} with response {response}")

    def remove_already_applied(self):
        self.vacancy_list = list(filter(lambda x: x["id"] not in self.applied_set, self.vacancy_list))
        logger.info(f"we got {len(self.vacancy_list)} not applied vacancies yet")

    def add_to_favorite_with_test(self):
        vacancy_to_add = list(filter(lambda x: x["has_test"], self.vacancy_list))
        logger.info(f" we got {len(vacancy_to_add)} vacancies with test")
        self.api_client.set_session_params({})
        for vacancy in vacancy_to_add:
            url = f"{basic_url}/vacancies/favorited/{vacancy['id']}"
            response: Response = self.api_client.safe_querry("PUT", url)
            if response.status_code == 204:
                logger.info(f"vacancy with id {vacancy['id']} added to favorite")
                self.applied_set.add(vacancy['id'])
            elif response.status_code in (403, 404):
                logger.warning(f"fail to add {vacancy['id']} to favorites")
                with open('add_to_favorite_with_test_errors.json', 'w') as file:
                    file.write(str(datetime.utcnow()))
                    json.dump(response.json(), file, separators=(',\n', ': '))
                    file.write("\n\n")
            else:
                logger.warning(f"fail to add {vacancy['id']} to favorites")
        self.vacancy_list = list(filter(lambda x: not x["has_test"], self.vacancy_list))

    def pickle_applied(self):
        filename = f"applied.pickle"
        fullfilepath = workdir.joinpath(filename)
        with open(fullfilepath, "wb") as file:
            pickle.dump(self.applied_set, file)
            logger.info(f"save binary file {fullfilepath}")

    def unpickle_applied(self):
        filename = f"applied.pickle"
        fullfilepath = workdir.joinpath(filename)
        if Path.exists(fullfilepath):
            with open(fullfilepath, "rb") as file:
                logger.info(f"open binary file {fullfilepath}")
                self.applied_set = pickle.load(file)

    def apply_without_letter(self):
        params = {"resume_id": resume_id}
        self.api_client.set_session_params(params)
        vacancies_to_apply = filter(lambda x: not x["response_letter_required"], self.vacancy_list)
        for vacancy in vacancies_to_apply:
            self.api_client.session.params["vacancy_id"] = vacancy["id"]
            response: Response = self.api_client.safe_querry("POST", self.url_for_apply)
            if response.status_code == 201:
                self.apply_counter += 1
                self.applied_set.add(vacancy['id'])
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
                self.applied_set.add(vacancy['id'])
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

    def normal_sequence(self, params: Params):
        self.search_vacancy(params)
        self.remove_already_applied()
        self.add_to_favorite_with_test()
        self.apply_without_letter()
        self.apply_with_letter()
        self.pickle_applied()



