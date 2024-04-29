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
    vacancy_manager.unpickle_applied()
    vacancy_manager.search_similar_vacancy()
    vacancy_manager.remove_already_applied()
    vacancy_manager.add_to_favorite_with_test()

    vacancy_manager.pickle_applied()

    # print(len(vacancy_manager.applied_set))
    # print(*vacancy_manager.applied_set, sep="  ")

    # vacancy_manager.apply_without_letter()
    # vacancy_manager.apply_with_letter()
    # print(len(vacancy_manager.vacancy_list))
    # print(*vacancy_manager.vacancy_list, sep="\n\n")

    # vacancy_manager.apply_without_letter()
    # vacancy_manager.apply_with_letter()




if __name__ == "__main__":
    main()


