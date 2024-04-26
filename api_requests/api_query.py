from loguru import logger
from requests import Session
from requests.models import Response

from tokens import tokens
from api_requests.retry import RetryManager
from basic_params import basic_timeout


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

    def unsafe_get(self, method: str, url: str, params: dict) -> Response:
        responce: Response = self.session.request(method,
                                                  url,
                                                  params=params,
                                                  timeout=basic_timeout,
                                                  allow_redirects=False)
        return responce

    def safe_get(self, method: str, url: str, params: dict) -> Response | None:
        logger.info(f"Try get data from {url}, with {method}")
        try:
            for attempt in self.retry_manager.make_retry():
                with attempt:
                    response: Response = self.unsafe_get(method, url, params)
                    return response
        except self.retry_error:
            logger.warning(f"out of retries with {method} request to {url}")
