from requests.models import Response
from loguru import logger

from api_requests.api_querry import ApiClient
from utils.basic_params import basic_url


class FavoritesHandler:
    def __init__(self, api_client):
        self.api_client: ApiClient = api_client
        self.url_for_apply: str = f"{basic_url}/vacancies/favorited"
        self.archived_favorites_list: list[dict | bool] = [True]
        self.favorite_params = {
            "page": 0,
            "per_page": 200,
        }


    def set_session_params(self, favorite_params):
        self.api_client.set_session_params(favorite_params)

    def get_favorite_list(self):
        response: Response = self.api_client.safe_querry("GET", self.url_for_apply)
        if response.status_code == 200:
            result = response.json()
            self.archived_favorites_list = list(filter(lambda x: x["archived"], result["items"]))
            logger.info(f"Got {len(self.archived_favorites_list)} archived "
                        f"favorite vacancies on {result['pages']}")
        else:
            pass

    def remove_archived_from_favorite(self, vacancy_id):
        response: Response = self.api_client.safe_querry("DELETE",
                                                         f"{self.url_for_apply}/{vacancy_id}")
        if response.status_code == 204:
            logger.info(f"Vacancy with id {vacancy_id} successfully removed")
        elif response.status_code == 403:
            logger.info(f"Current user is not applicant")
        elif response.status_code == 404:
            logger.info(f"Vacancy with id {vacancy_id} is not found")


    def run(self):
        while self.archived_favorites_list:
            self.set_session_params(self.favorite_params)
            self.get_favorite_list()
            for archived in self.archived_favorites_list:
                self.remove_archived_from_favorite(archived["id"])

