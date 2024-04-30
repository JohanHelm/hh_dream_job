import pytest

from api_requests.api_querry import ApiClient
from secrets.tokens import tokens
from utils.basic_params import basic_url


def test_check_tokens_handler_attrs(create_tokens_handler):
    attributes = create_tokens_handler.__dict__
    assert isinstance(attributes["api_client"], ApiClient) \
           and attributes["tokens"] == tokens \
           and attributes["url"] == f"{basic_url}/token"


def test_check_valid_access_token(create_tokens_handler):
    assert create_tokens_handler.check_valid_access_token()
