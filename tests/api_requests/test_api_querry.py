import pytest
from requests import Session
from requests.exceptions import ConnectionError
from requests.models import Response
from tenacity import RetryError

from api_requests.retry import RetryManager
from secrets.tokens import tokens


def test_check_api_client_attrs(create_api_client):
    attributes = create_api_client.__dict__
    assert isinstance(attributes["session"], Session) \
           and isinstance(attributes["retry_manager"], RetryManager) \
           and attributes["retry_error"] is RetryError


def test_check_api_client_session_headers(create_api_client):
    headers = {'User-Agent': 'python-requests/2.31.0',
               'Accept-Encoding': 'gzip, deflate',
               'Accept': '*/*',
               'Connection': 'keep-alive',
               'Authorization': f'Bearer {tokens["access_token"]}',
               }

    assert create_api_client.session.headers == headers


def test_set_api_client_session_params(create_api_client):
    params = {"param_key": "param_value"}
    create_api_client.set_session_params(params)
    assert create_api_client.session.params == params


def test_api_client_unsafe_querry(create_api_client):
    response: Response = create_api_client.unsafe_querry(method="GET", url="https://ifconfig.me")
    assert response.status_code == 200


@pytest.mark.slow
def test_api_client_safe_querry(create_api_client):
    with pytest.raises(ConnectionError):
        create_api_client.safe_querry(method="GET", url="https://bad-url.com")



