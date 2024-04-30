import pytest

from api_requests.api_querry import ApiClient
from utils.tokens_handler import TokensHandler
from operations.vacancy_handler import ApplicantManager


@pytest.fixture(scope='session')
def create_api_client():
    api_client = ApiClient()
    return api_client


@pytest.fixture(scope='session')
def create_tokens_handler(create_api_client):
    tokens_handler = TokensHandler(create_api_client)
    return tokens_handler


@pytest.fixture(scope='session')
def create_vacancy_manager(create_api_client):
    vacancy_manager = ApplicantManager(create_api_client)
    return vacancy_manager
