import json
from datetime import datetime, UTC
from typing import Any

from loguru import logger
from requests import Response

from api_requests.api_querry import ApiClient
from utils.basic_params import basic_url


class DiscardsRemover:
    def __init__(self, api_client):
        self.url_for_apply = f"{basic_url}/negotiations"
        self.api_client: ApiClient = api_client
        self.discard_params = {
            "order_by": "updated_at",
            "order": "asc",
            "status": "discard",
            "page": 0,
        }
        self.found = 1

    def set_session_params(self):
        self.api_client.set_session_params(self.discard_params)

    def search_discarded_applies(self):
        while self.found:
            response: Response = self.api_client.safe_querry("GET", self.url_for_apply)
            if response.status_code == 200:
                result = response.json()
                logger.info(
                    f"found by discard apply search {result['found']} discards in {result['pages']} pages")
                self.found = result['found']
                self.remove_discarded_applies(result["items"])

            elif response.status_code in (400, 404):
                logger.warning(f"failure to search in discard apply search with response {response}")
                with open(f'search_discard_apply_errors.json', 'w') as file:
                    file.write(f"{datetime.now(UTC)}\n")
                    json.dump(response.json(), file, separators=(',\n', ': '))
                    file.write("\n\n")
            elif response.status_code in 403:
                logger.warning(f"failure to search in discard apply search with response {response}")
                with open(f'search_discard_apply_errors.json', 'w') as file:
                    file.write(f"{datetime.now(UTC)}\n")
                    json.dump(response.json(), file, separators=(',\n', ': '))
                    file.write("\n\n")
                self.found = 0
            else:
                logger.warning(f"failure to search in discard apply search with response {response}")

    def remove_discarded_applies(self, applies_list: list[dict[Any]]):
        for apply in applies_list:
            response: Response = self.api_client.safe_querry("DELETE", f"{self.url_for_apply}/active/{apply['id']}")
            if response.status_code == 204:
                pass
            elif response.status_code in (425, 403, 404):
                logger.warning(f"failure to remove discarded apply with response {response}")
                with open(f'remove_discard_apply_errors.json', 'w') as file:
                    file.write(f"{datetime.now(UTC)}\n")
                    json.dump(response.json(), file, separators=(',\n', ': '))
                    file.write("\n\n")
            else:
                logger.warning(f"failure to  remove discarded apply with response {response}")

    def run(self):
        self.set_session_params()
        self.search_discarded_applies()
