import requests
from requests import Response
from datetime import datetime

from secrets.client_secrets import client_secret, client_id
from utils.basic_params import basic_url


def save_tokens(response: Response):
    tokens = response.json()
    expires_at = datetime.timestamp(datetime.utcnow()) + tokens["expires_in"]
    tokens["expires_at"] = expires_at
    file_with_tokens = f'../secrets/tokens.py'
    with open(file_with_tokens, 'w', encoding='utf-8') as file:
        file.write(f'tokens = {tokens}')


def get_tokens(code: str):
    params = {"client_id": client_id,
              "client_secret": client_secret,
              "code": code,
              "grant_type": "authorization_code",
              }
    response: Response = requests.post(f"{basic_url}/token", params=params)
    save_tokens(response)


get_tokens(code="")
