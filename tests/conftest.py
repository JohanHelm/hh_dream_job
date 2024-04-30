import pytest

from api_requests.api_querry import ApiClient
from utils.tokens_handler import TokensHandler


@pytest.fixture(scope='session')
def create_api_client():
    api_client = ApiClient()
    return api_client


@pytest.fixture(scope='session')
def create_tokens_handler(create_api_client):
    tokens_handler = TokensHandler(create_api_client)
    return tokens_handler
