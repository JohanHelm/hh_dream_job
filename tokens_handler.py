import requests
from requests import Response
from datetime import datetime
from time import sleep

from secrets import client_secret, client_id
from tokens import tokens
from basic_params import basic_url, basic_headers


class TokensHandler:
    def __init__(self):
        self.tokens = tokens
        self.url = f"{basic_url}/token"
        self.headers = basic_headers

    def get_tokens(self, code: str):
        params = {"client_id": client_id,
                  "client_secret": client_secret,
                  "code": code,
                  "grant_type": "authorization_code",
                  }
        response: Response = requests.post(self.url, headers=self.headers, params=params)
        self.save_tokens(response)

    def save_tokens(self, response: Response):
        tokens = response.json()
        # expires_at = datetime.utcnow() + timedelta(seconds=tokens["expires_in"])
        expires_at = datetime.timestamp(datetime.utcnow()) + tokens["expires_in"]
        tokens["expires_at"] = expires_at
        self.tokens = tokens
        file_with_tokens = f'tokens.py'
        with open(file_with_tokens, 'w', encoding='utf-8') as file:
            # file.write("import datetime")
            # file.write("\n\n")
            file.write(f'tokens = {self.tokens}')

    def valid_tokens(self) -> bool:
        token_live_left = self.tokens["expires_at"] - datetime.timestamp(datetime.utcnow())
        return token_live_left > 60

    def update_tokens(self):
        params = {"grant_type": "refresh_token",
                  "refresh_token": self.tokens["refresh_token"]
                  }
        response: Response = requests.post(self.url, headers=self.headers, params=params)
        self.save_tokens(response)

    def give_valid_access_token(self):
        if not self.valid_tokens():
            sleep(60)
            self.update_tokens()
        return self.tokens["access_token"]
