import pickle
from pathlib import Path

from utils.basic_params import basic_url, workdir
from operations.applicant_params import applicant_params


def test_check_vacancy_handler_attrs(create_vacancy_manager, create_api_client):
    attributes = {'url_for_apply': f'{basic_url}/negotiations',
                  'search_step': 0,
                  'pages_found': 1,
                  'apply_counter': 0,
                  'apply_limit': 195,
                  'api_client': create_api_client,
                  'vacancy_list': [],
                  'applied_set': set(),
                  'bad_companies': set()}
    assert create_vacancy_manager.__dict__ == attributes


def test_unpickle_applied(create_vacancy_manager):
    filename = f"applied.pickle"
    fullfilepath = workdir.joinpath(filename)
    if Path.exists(fullfilepath):
        with open(fullfilepath, "rb") as file:
            applied_set = pickle.load(file)

    create_vacancy_manager.unpickle_applied()
    assert create_vacancy_manager.applied_set == applied_set


def test_unpickle_bad_companies(create_vacancy_manager):
    filename = f"bad_companies.pickle"
    fullfilepath = workdir.joinpath(filename)
    if Path.exists(fullfilepath):
        with open(fullfilepath, "rb") as file:
            bad_companies = pickle.load(file)

    create_vacancy_manager.unpickle_bad_companies()
    assert create_vacancy_manager.bad_companies == bad_companies


def test_search_vacancy(create_vacancy_manager):
    create_vacancy_manager.search_vacancy(applicant_params[4])
    assert create_vacancy_manager.vacancy_list


def test_remove_already_applied(create_vacancy_manager):
    create_vacancy_manager.remove_already_applied()
    assert all([item['id'] not in create_vacancy_manager.applied_set
                for item in create_vacancy_manager.vacancy_list])


def test_remove_bad_companies(create_vacancy_manager):
    create_vacancy_manager.remove_bad_companies()
    assert all([item["employer"]["id"] not in create_vacancy_manager.bad_companies
                for item in create_vacancy_manager.vacancy_list])


def test_add_to_favorite_with_test(create_vacancy_manager):
    len_before_add = len(create_vacancy_manager.vacancy_list)
    len_vacancy_to_add = len(list(filter(lambda x: x["has_test"], create_vacancy_manager.vacancy_list)))
    create_vacancy_manager.add_to_favorite_with_test()
    assert len(create_vacancy_manager.vacancy_list) == len_before_add - len_vacancy_to_add




