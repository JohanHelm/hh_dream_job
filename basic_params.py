from pathlib import Path


workdir: Path = Path(__file__).resolve().parent

basic_url = "https://api.hh.ru"

basic_timeout = 3

# params for similar search
search_params_1 = {"page": 0,
                 "per_page": 100,
                 "text": "Python",
                 "search_field": ("name", "description"),
                 "experience": ("noExperience", "between1And3"),
                 # "employment": ("full", "part", "project"),
                 # "schedule":  ("fullDay", "shift", "flexible", "remote"),
                 # "area": 113,  # Russia 113, Tomsk area 1255, Tomsk 90,
                 # "area": 1255,
                 # "professional_role": 96,
                 # "professional_role": (96, 160, 124, 112, 113, 121), {'96': 'Программист, разработчик', '160': 'DevOps-инженер', '124': 'Тестировщик', '112': 'Сетевой инженер', '113': 'Системный администратор', '121': 'Специалист технической поддержки'}

                 # "period": 30,
                 "order_by": "publication_time",
                 }

# first common search
search_params_2 = {"page": 0,
                 "per_page": 100,
                 "text": "Python",
                 "search_field": ("name", "description"),
                 "experience": ("noExperience", "between1And3"),
                 # "employment": ("full", "part", "project"),
                 # "schedule":  ("fullDay", "shift", "flexible", "remote"),
                 "area": 1255,
                 # "professional_role": (96, 160, 124, 112, 113, 121),
                 # "period": 30,
                 "order_by": "publication_time",
                 }

# second common search
search_params_3 = {"page": 0,
                 "per_page": 100,
                 "text": "Python",
                 "search_field": ("name", "description"),
                 "experience": ("noExperience", "between1And3"),
                 # "employment": ("full", "part", "project"),
                 "schedule":  ("flexible", "remote"),
                 # "area": 1255,
                 # "professional_role": (96, 160, 124, 112, 113, 121),
                "professional_role": 96,
                 "period": 30,
                 "order_by": "publication_time",
                 }



def create_response_letter(vacancy_url: str, vacancy_name: str, ):
    return f"Здравствуйте,\n\nМеня зовут Александр, я Python Backend Developer. " \
           f"Я пишу вам, чтобы выразить свой интерес к вакансии {vacancy_name}, " \
           f"размещенной по следующей ссылке {vacancy_url}. " \
           f"Я убежден, что мой опыт и навыки могут значительно внести пользу в вашу команду.\n\n" \
           f"Позвольте мне рассказать вам о причинах моего желания сменить профессию. " \
           f"В течение более чем 20 лет я приобрел опыт в области нефтепереработки и нефтехимии, " \
           f"на протяжении этого времени я выполнял работу на рабочих, а затем и на руководящих позициях. " \
           f"Руководил коллективами до 25 человек, дорос до должности начальника цеха." \
           f"Однако, с течением времени я осознал, что мои интересы и страсти лежат в другой сфере, " \
           f"а именно в сфере программирования.\n\n" \
           f"С 2020 года я начал самостоятельное обучение, по таким IT дисциплинам как информатика, сети, " \
           f"linux, bash, python. Благодаря моей самодисциплине, организованности и целеустремлённости я достиг " \
           f"заметных результатов в освоении новой профессии." \
           f"Я уверен, что моя предыдущая профессиональная подготовка " \
           f"в области химических производств и новые навыки, " \
           f"которые я приобрел, помогут мне эффективно выполнять задачи в вашей компании.\n\n" \
           f"Прикладываю своё резюме. С моими проектами на гитхабе можно ознакомиться " \
           f"по ссылке https://github.com/JohanHelm\n"  \
           f"Если у вас есть какие - то вопросы, с удовольствием на них отвечу. " \
           f"Так же я готов выполнить любое тестовое задание." \
           f"Буду рад любой обратной связи.\n\n" \
           f"До свидания:)"
