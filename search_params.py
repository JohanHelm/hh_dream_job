from dataclasses import dataclass


@dataclass()
class SearchParams:
    page: int = 0
    per_page: int = 100
    text: str = "Python"
    search_field: tuple[str, ...] = ("name", "description")
    experience: tuple[str, ...] = ("noExperience", "between1And3")
    # employment: tuple[str, ...] = ('full', 'part', 'project')
    # schedule: tuple[str, ...] = ('fullDay', 'shift', 'flexible', 'remote')
    area: int = 113  # Russia 113, Tomsk area 1255, Tomsk 90
    # professional_role: int | tuple[int] = (96, 160, 124, 112, 113, 121)
    # period: int = 30
    order_by: str = "publication_time"

    # ({'id': '160', 'name': 'DevOps-инженер'},
    # {'id': '96', 'name': 'Программист, разработчик'},
    # {'id': '112', 'name': 'Сетевой инженер'},
    # {'id': '113', 'name': 'Системный администратор'},
    # {'id': '121', 'name': 'Специалист технической поддержки'},
    # {'id': '124', 'name': 'Тестировщик'})


# tomsk_search_params = {"page": 0,
#                        "per_page": 100,
#                        "text": "Python",
#                        "search_field": ("name", "description"),
#                        "experience": ("noExperience", "between1And3"),
#                        "employment": ('full', 'part', 'project'),
#                        "schedule": ('fullDay', 'shift', 'flexible', 'remote'),
#                        "area": 1255, # Russia 113, Tomsk area 1255, Tomsk 90
#                        "professional_role": 96, #({'id': '160', 'name': 'DevOps-инженер'},
#                                                 # {'id': '96', 'name': 'Программист, разработчик'},
#                                                 # {'id': '112', 'name': 'Сетевой инженер'},
#                                                 # {'id': '113', 'name': 'Системный администратор'},
#                                                 # {'id': '121', 'name': 'Специалист технической поддержки'},
#                                                 # {'id': '124', 'name': 'Тестировщик'})
#                        "period": 2,
#                        "order_by": "publication_time",
#                        }
