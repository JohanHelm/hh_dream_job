import json
from requests import Response
from datetime import datetime
from time import sleep
from loguru import logger

from api_requests.api_querry import ApiClient
from secrets.tokens import tokens
from utils.basic_params import basic_url


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

    def update_tokens(self):
        params = {"grant_type": "refresh_token",
                  "refresh_token": self.tokens["refresh_token"]
                  }
        self.api_client.set_session_params(params)
        response: Response = self.api_client.safe_querry("POST", self.url)
        update_successfull = False
        if response.status_code == 200:
            self.save_tokens(response)
            self.api_client.update_session_headers()
            logger.info("access token been successfully updated")
            update_successfull = True
        elif response.status_code in (400, 403):
            logger.warning(f"failure to update tokens with response {response}")
            with open('update_token_errors.json', 'w') as file:
                file.write(str(datetime.utcnow()))
                json.dump(response.json(), file, separators=(',\n', ': '))
                file.write("\n\n")
        else:
            logger.warning(f"failure to update tokens with response {response}")
        return update_successfull

    def check_valid_access_token(self):
        token_valid = True
        token_live_left = self.tokens["expires_at"] - datetime.timestamp(datetime.utcnow())
        if token_live_left <= 60:
            logger.info("access token got old, trying to refresh it")
            sleep(60)
            token_valid = self.update_tokens()
        return token_valid
