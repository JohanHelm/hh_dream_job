import json
import pickle
from datetime import datetime, UTC
from pathlib import Path

from loguru import logger
from requests import Response

from api_requests.api_querry import ApiClient
from operations.applicant_params import Params, applicant_params
from secrets.client_secrets import resume_id
from utils.basic_params import basic_url, create_response_letter, workdir


class ApplicantManager:
    def __init__(self, api_client):
        self.url_for_apply = f"{basic_url}/negotiations"
        self.search_step: int = 0
        self.pages_found: int = 1
        self.apply_counter: int = 0
        self.apply_limit: int = 195
        self.api_client: ApiClient = api_client
        self.vacancy_list: list[dict] = []
        self.applied_set: set[str] = set()
        self.bad_companies: set[str] = set()
        self.bad_vacancy_names: set[str] = set()

    def search_vacancy(self, params: Params):
        self.api_client.set_session_params(params.search_params)
        response: Response = self.api_client.safe_querry("GET", params.search_url)
        if response.status_code == 200:
            result = response.json()
            logger.info(f"found by {params.search_mode} search {result['found']} vacancies in {result['pages']} pages")
            self.pages_found = result["pages"]
            self.vacancy_list = result["items"]
        elif response.status_code in (400, 403, 404):
            logger.warning(f"failure to search in {params.search_mode} with response {response}")
            with open(f'search_{params.search_mode}_vacancy_errors.json', 'w') as file:
                file.write(f"{datetime.now(UTC)}\n")
                json.dump(response.json(), file, separators=(',\n', ': '))
                file.write("\n\n")
        else:
            logger.warning(f"failure to search in {params.search_mode} with response {response}")

    def remove_already_applied(self):
        self.vacancy_list = list(filter(lambda x: x["id"] not in self.applied_set, self.vacancy_list))
        logger.info(f"we got {len(self.vacancy_list)} not applied vacancies yet")

    def remove_bad_companies(self):
        self.vacancy_list = list(filter(lambda x: x["employer"]["name"] not in self.bad_companies, self.vacancy_list))
        logger.info(f"we got {len(self.vacancy_list)} vacancies from good companies")

    def check_vacancy_has_good_name(self, vacancy: dict[...]) -> bool:
        for bad_name in self.bad_vacancy_names:
            if bad_name in vacancy["name"].lower():
                return False
        return True

    def remove_bad_vacancy_names(self):
        self.vacancy_list = list(filter(self.check_vacancy_has_good_name, self.vacancy_list))
        logger.info(f"we got {len(self.vacancy_list)} vacancies with good names")

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
                    file.write(f"{datetime.now(UTC)}\n")
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
        logger.info(f"we got {len(self.applied_set)} already applied vacancies after bot working")

    def unpickle_applied(self):
        filename = f"applied.pickle"
        fullfilepath = workdir.joinpath(filename)
        if Path.exists(fullfilepath):
            with open(fullfilepath, "rb") as file:
                logger.info(f"open binary file {fullfilepath}")
                self.applied_set = pickle.load(file)
        logger.info(f"we got {len(self.applied_set)} already applied vacancies before bot working")

    def unpickle_bad_companies(self):
        filename = f"bad_companies.pickle"
        fullfilepath = workdir.joinpath(filename)
        if Path.exists(fullfilepath):
            with open(fullfilepath, "rb") as file:
                logger.info(f"open binary file {fullfilepath}")
                self.bad_companies = pickle.load(file)
        logger.info(f"we got {len(self.bad_companies)} bad companies for now")

    def unpickle_bad_vacancy_names(self):
        filename = f"bad_vacancy_names.pickle"
        fullfilepath = workdir.joinpath(filename)
        if Path.exists(fullfilepath):
            with open(fullfilepath, "rb") as file:
                logger.info(f"open binary file {fullfilepath}")
                self.bad_vacancy_names = pickle.load(file)
        logger.info(f"we got {len(self.bad_vacancy_names)} bad vacancy names for now")

    def apply(self, letter: bool = False):
        self.api_client.set_session_params({"resume_id": resume_id})
        vacancies_to_apply = filter(lambda x: x["response_letter_required"] is letter, self.vacancy_list)
        for vacancy in vacancies_to_apply:
            self.api_client.session.params["vacancy_id"] = vacancy["id"]
            if letter:
                self.api_client.session.params["message"] = create_response_letter(vacancy_url=vacancy["alternate_url"],
                                                                                   vacancy_name=vacancy["name"])
            response: Response = self.api_client.safe_querry("POST", self.url_for_apply)
            if response.status_code == 201:
                self.apply_counter += 1
                self.applied_set.add(vacancy['id'])
                if self.apply_counter == self.apply_limit:
                    logger.info(f"exceed apply limit for today")
                    break
            elif response.status_code in (403, 400):
                result = response.json()
                if result["description"] == "Already applied":
                    self.applied_set.add(vacancy['id'])
                elif result["description"] == "Daily negotiations limit is exceeded":
                    logger.warning(f"we got out of applies for today!!!")
                    self.apply_counter = self.apply_limit
                    break
                else:
                    logger.warning(f"failure to appy vacancy {vacancy['id']} with response {response}")
                    with open('apply_errors.json', 'a') as file:
                        file.write(f"{datetime.now(UTC)}\n")
                        file.write(f"{vacancy['id']}\n")
                        json.dump(result, file, separators=(',\n', ': '))
                        file.write("\n\n")
            else:
                logger.warning(f"failure to apply vacancy {vacancy['id']} with response {response}")
        logger.info(f"total apply with {letter} letter is {self.apply_counter}")

    def normal_sequence(self, params: Params):
        self.search_vacancy(params)
        self.remove_already_applied()
        self.remove_bad_companies()
        self.remove_bad_vacancy_names()
        self.add_to_favorite_with_test()
        self.apply()
        self.apply(letter=True)

    def run(self):
        self.unpickle_applied()
        self.unpickle_bad_companies()
        self.unpickle_bad_vacancy_names()
        while self.apply_counter < self.apply_limit:
            logger.info(f"starting {self.search_step} step with {self.apply_counter} apply_counter")
            try:
                params = applicant_params[self.search_step]
            except IndexError:
                logger.warning(f"applicant_params is too short, need much more!!!")
                break
            else:
                self.normal_sequence(params)
                if self.pages_found > 1:
                    for page in range(1, self.pages_found):
                        logger.info(f"searching on page {page}")
                        params.search_params["page"] = page
                        self.normal_sequence(params)
                self.search_step += 1
        self.pickle_applied()
        logger.info(f"bot finish working with {self.search_step} step and {self.apply_counter} apply_counter")
