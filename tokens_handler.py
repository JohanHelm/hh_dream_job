import json
from requests import Response
from datetime import datetime
from time import sleep
from loguru import logger

from api_requests.api_query import ApiClient
from secrets.tokens import tokens
from basic_params import basic_url


class TokensHandler:
    def __init__(self, api_client):
        self.api_client: ApiClient = api_client
        self.tokens = tokens
        self.url = f"{basic_url}/token"

    def save_tokens(self, response: Response):
        tokens = response.json()
        expires_at = datetime.timestamp(datetime.utcnow()) + tokens["expires_in"]
        tokens["expires_at"] = expires_at
        self.tokens = tokens
        file_with_tokens = f'secrets/tokens.py'
        with open(file_with_tokens, 'w', encoding='utf-8') as file:
            file.write(f'tokens = {self.tokens}')
        logger.info("new token saved to file")

    def valid_tokens(self) -> bool:
        token_live_left = self.tokens["expires_at"] - datetime.timestamp(datetime.utcnow())
        return token_live_left > 60

    def update_tokens(self):
        params = {"grant_type": "refresh_token",
                  "refresh_token": self.tokens["refresh_token"]
                  }
        self.api_client.set_session_params(params)
        response: Response = self.api_client.safe_querry("POST", self.url)
        if response.status_code == 200:
            self.save_tokens(response)
            self.api_client.update_session_headers()
            logger.info("access token been successfully updated")
        elif response.status_code in (400, 403):
            logger.warning(f"failure to update tokens with response {response}")
            with open('update_token_errors.json', 'w') as file:
                file.write(str(datetime.utcnow()))
                json.dump(response.json(), file, separators=(',\n', ': '))
                file.write("\n\n")
            quit()
        else:
            logger.warning(f"failure to update tokens with response {response}")
            quit()

    def check_valid_access_token(self):
        if not self.valid_tokens():
            logger.info("access token got old, trying to refresh it")
            sleep(60)
            self.update_tokens()
