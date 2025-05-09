from time import perf_counter

from utils.logging_settings import init_logger, configure_logger
from api_requests.api_querry import ApiClient
from utils.tokens_handler import TokensHandler
from utils.basic_params import duration
from operations.vacancy_handler import ApplicantManager
from operations.applies_ops import DiscardsRemover
from operations.favorites_ops import FavoritesHandler


def main():
    start = perf_counter()
    logger = init_logger()
    configure_logger(logger, file_path="logs/logfile.log", rotation=10)
    api_client = ApiClient()
    tokens_handler = TokensHandler(api_client)

    if tokens_handler.check_valid_access_token():
        discard_remover = DiscardsRemover(api_client)
        discard_remover.run()
        favorites_handler = FavoritesHandler(api_client)
        favorites_handler.run()
        vacancy_manager = ApplicantManager(api_client)
        vacancy_manager.run()
    else:
        logger.warning(f"some huge problem with tokens update")
    end = perf_counter()
    logger.info(f"Full time spent for apply is {duration(start, end)}")


if __name__ == "__main__":
    main()
