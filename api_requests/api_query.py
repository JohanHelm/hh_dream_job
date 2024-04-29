from loguru import logger
from requests import Session
from requests.models import Response

from secrets.tokens import tokens
from api_requests.retry import RetryManager
from utils.basic_params import basic_timeout


class ApiClient:
    def __init__(self):
        self.session = Session()
        self.retry_manager: RetryManager = RetryManager()
        self.retry_error = self.retry_manager.retry_error
        self.update_session_headers()
        logger.info("init ApiClient")

    def update_session_headers(self):
        self.session.headers.update({"Authorization": f'Bearer {tokens["access_token"]}'})
        logger.info("session headers has successfully updated")

    def set_session_params(self, params):
        self.session.params = params

    def unsafe_querry(self, method: str, url: str) -> Response:
        responce: Response = self.session.request(method,
                                                  url,
                                                  timeout=basic_timeout,
                                                  allow_redirects=False)
        return responce

    def safe_querry(self, method: str, url: str) -> Response | None:
        logger.info(f"Try get data from {url}, with {method}")
        try:
            for attempt in self.retry_manager.make_retry():
                with attempt:
                    response: Response = self.unsafe_querry(method, url)
                    return response
        except self.retry_error:
            logger.warning(f"out of retries with {method} request to {url}")
