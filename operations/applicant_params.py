from collections import namedtuple

from secrets.client_secrets import resume_id
from utils.basic_params import basic_url

Params = namedtuple('Params', ('search_mode', 'search_url', 'search_params'))

similar_search_url = f"{basic_url}/resumes/{resume_id}/similar_vacancies"
common_search_url = f"{basic_url}/vacancies"

search_text = "Python"

search_field = (
    "name",
    "description",
)

experience = (
    "between1And3",
)

employment = (
    "full",
    "part",
    "project",
)

schedule = (
    "fullDay",
    "shift",
    "flexible",
    "remote"
)

area = {
    "Russia": 113,
    "Tomsk area": 1255,
    "Tomsk": 90,
}

professional_role = {
    "Программист, разработчик": 96 ,
    "DevOps-инженер": 160,
    "Тестировщик": 124,
    "Сетевой инженер": 112,
    "Системный администратор": 113,
    "Специалист технической поддержки": 121,
}

full_search_params = {"page": 0,
                      "per_page": 100,
                      "text": search_text,
                      "search_field": ("name", "description"),
                      "experience": experience,
                      "employment": employment,
                      "schedule": schedule,
                      "area": area,
                      "professional_role": professional_role.values(),
                      "period": 30,
                      "order_by": "publication_time",
                      }

# params for similar search
search_params_1 = {"page": 0,
                   "per_page": 100,
                   "text": search_text,
                   "search_field": ("name", "description"),
                   "experience": experience,
                   "order_by": "publication_time",
                   }

# params for similar search
search_params_2 = {"page": 0,
                   "per_page": 100,
                   "professional_role": (
                       professional_role["Программист, разработчик"],
                       professional_role["DevOps-инженер"],
                       professional_role["Тестировщик"],
                   ),
                   "experience": experience,
                   "order_by": "publication_time",
                   }

# first common search
search_params_3 = {"page": 0,
                   "per_page": 100,
                   "text": search_text,
                   "search_field": ("name", "description"),
                   "experience": experience,
                   "area": area["Tomsk area"],
                   "professional_role": (
                       professional_role["Программист, разработчик"],
                       professional_role["DevOps-инженер"],
                       professional_role["Тестировщик"],
                   ),
                   "order_by": "publication_time",
                   }

# second common search
search_params_4 = {"page": 0,
                   "per_page": 100,
                   "text": search_text,
                   "search_field": ("name", "description"),
                   "experience": experience,
                   "employment": employment,
                   "schedule": ("flexible", "remote"),
                   "professional_role": professional_role["Программист, разработчик"],
                   "order_by": "publication_time",
                   }

# third common search
search_params_5 = {"page": 0,
                   "per_page": 100,
                   "text": search_text,
                   "search_field": ("name", "description"),
                   "experience": experience,
                   "employment": employment,
                   "schedule": ("flexible", "remote"),
                   "professional_role": (
                       professional_role["DevOps-инженер"],
                       professional_role["Тестировщик"],
                   ),
                   "order_by": "publication_time",
                   }

# third common search
search_params_6 = {"page": 0,
                   "per_page": 100,
                   "text": search_text,
                   "search_field": ("name", "description"),
                   "experience": experience,
                   "employment": employment,
                   "professional_role": professional_role["Программист, разработчик"],
                   "order_by": "publication_time",
                   }

applicant_params = (Params("similar", similar_search_url, search_params_1),
                    Params("similar", similar_search_url, search_params_2),
                    Params("common", common_search_url, search_params_3),
                    Params("common", common_search_url, search_params_4),
                    Params("common", common_search_url, search_params_5),
                    Params("common", common_search_url, search_params_6),
                    )
