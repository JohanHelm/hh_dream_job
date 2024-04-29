from collections import namedtuple

from utils.basic_params import basic_url
from secrets.client_secrets import resume_id

Params = namedtuple('Params', ('search_mode', 'search_url', 'search_params'))

similar_search_url = f"{basic_url}/resumes/{resume_id}/similar_vacancies"
common_search_url = f"{basic_url}/vacancies"

full_search_params = {"page": 0,
                      "per_page": 100,
                      "text": "Python",
                      "search_field": ("name", "description"),
                      "experience": ("noExperience", "between1And3"),
                      "employment": ("full", "part", "project"),
                      "schedule":  ("fullDay", "shift", "flexible", "remote"),
                      "area": 113,  # Russia 113, Tomsk area 1255, Tomsk 90,
                      "professional_role": (96, 160, 124, 112, 113, 121),
                      # {'96': 'Программист, разработчик',
                      # '160': 'DevOps-инженер',
                      # '124': 'Тестировщик',
                      # '112': 'Сетевой инженер',
                      # '113': 'Системный администратор',
                      # '121': 'Специалист технической поддержки'}
                      "period": 30,
                      "order_by": "publication_time",
                      }

# params for similar search
search_params_1 = {"page": 0,
                   "per_page": 100,
                   "text": "Python",
                   "search_field": ("name", "description"),
                   "experience": ("noExperience", "between1And3"),
                   "order_by": "publication_time",
                   }

# first common search
search_params_2 = {"page": 0,
                   "per_page": 100,
                   "text": "Python",
                   "search_field": ("name", "description"),
                   "experience": ("noExperience", "between1And3"),
                   "area": 1255,
                   "order_by": "publication_time",
                   }

# second common search
search_params_3 = {"page": 0,
                   "per_page": 100,
                   "text": "Python",
                   "search_field": ("name", "description"),
                   "experience": ("noExperience", "between1And3"),
                   "schedule": ("flexible", "remote"),
                   "professional_role": 96,
                   "order_by": "publication_time",
                   }


applicant_params = (Params("similar", similar_search_url, search_params_1),
                    Params("common", common_search_url, search_params_2),
                    Params("common", common_search_url, search_params_3)
                    )
