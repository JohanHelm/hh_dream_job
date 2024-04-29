from utils.logging_settings import init_logger, configure_logger
from api_requests.api_query import ApiClient
from utils.tokens_handler import TokensHandler
from operations.vacancy_handler import ApplicantManager


def main():
    logger = init_logger()
    configure_logger(logger, file_path="logs/logfile.log", rotation=10)
    api_client = ApiClient()
    tokens_handler = TokensHandler(api_client)

    tokens_handler.check_valid_access_token()
    vacancy_manager = ApplicantManager(api_client)
    vacancy_manager.run()


if __name__ == "__main__":
    main()


