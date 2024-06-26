from pathlib import Path


workdir: Path = Path(__file__).resolve().parent.parent

basic_url = "https://api.hh.ru"

basic_timeout = 3


def duration(start, end):
    seconds = end - start
    hours = int(seconds // 3600)
    seconds %= 3600
    minutes = int(seconds // 60)
    seconds = int(seconds % 60)
    return f"{hours:02d}:{minutes:02d}:{seconds:02d}"


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
