from requests import Response, Session
from pathlib import Path
import pickle

from secrets.tokens import tokens
from utils.basic_params import workdir


filename = f"bad_companies.pickle"
fullfilepath = workdir.joinpath(filename)
print(fullfilepath)

if Path.exists(fullfilepath):
    with open(fullfilepath, "rb") as file:
        bad_companies_set = pickle.load(file)

else:
    bad_companies_set = set()

print(len(bad_companies_set))
print(*sorted(bad_companies_set), sep="\n")
url = "https://api.hh.ru/employers"
headers = {'Authorization': f'Bearer {tokens["access_token"]}'}

search_params = {"page": 0,
                 "per_page": 100,
                 "text": "СибГМУ",
                 # "search_field": "company_name",
                 }

session = Session()
session.headers.update(headers)
session.params = search_params

response: Response = session.get(url)
result = response.json()

companies = result["items"]
for company in companies:
    print(company)
    bad_companies_set.add(company['name'])


bad_company_names = ('Компьютерная Академия Top',
                     'Компьютерная Академия IT STEP',
                     'Школа программирования JETCODE',
                     'Онлайн-школа Тетрика',
                     'Школа 21',
                     'Компьютерная школа IT-Compot',
                     'Детская школа программирования Софтиум',
                     'ЧУ ДО Московская школа программистов',
                     'Школа программирования Креайтивика',
                     'Школа программирования для детей Code-Class',
                     'Школа программирования Kodland',
                     'Студсервис',
                     'Айтигенио',
                     'ITSTEP Academy Almaty',
                     'Ворк5',
                     'Homework',
                     'EasyCode',
                     'Skyeng',
                     'LATOKEN',
                     'IT школа Hello world',
                     'Хэппи Студент',
                     'ДИСЕНТ',
                     'Таранюк Виталий Геннадьевич',
                     'Nexpanse',
                     'DocuSketch',
                     'JustCode',
                     'Центр финансовых технологий',
                     'Kiberone (ИП Евсенин Алексей Сергеевич)',
                     'KIBERone (ИП Григорян Николай Ашотович)',
                     'KIBERone (ИП Демиденко Анастасия Юрьевна)',
                     'KIBERone (ИП Павловский Станислав Александрович)',
                     'KIBERONE (ИП Модова Юлия Викторовна)',
                     'KiberOne (ИП Зивтинь Мария Олеговна)',
                     'KiberOne (Ип Новосельцев Сергей Александрович)',
                     'KIBERONE (ИП Модова Юлия Викторовна)',
                     'KIBERone (ИП Пальцева Татьяна Викторовна)',
                     'KIBERone (Митрофанова Ксения Владимировна)',
                     'KIBERone (ИП Коростелева Татьяна Олеговна)',
                     'KIBERone (ИП Янкевич Олег Станиславович)',
                     'KIBERone (ИП Ерошкин Данил Сергеевич)',
                     'KiberOne (ИП Докучаева Юлия Викторовна)',
                     'KIBERone (ИП Белоусова Олеся Сергеевна)',
                     'KIBERone (ИП Лисицкий Ян Сергеевич)',
                     'KIBERone (ИП Решетникова Валерия Николаевна)',
                     'KIBERone Aksay (Баймуканов А. С)',
                     'K1berOne (ИП Гаюн Артем Сергеевич)',
                     'КиберШкола KIBERone (ИП Коваленко Дмитрий Валерьевич)',
                     'Пучкова Софья Денисовна',
                     'Школа иновации Новое поколение',
                     'АЙТИ ШАГ',
                     'Алгоритмика Б',
                     'Tibbo',
                     "Гилядов Гиляд Перисович",
                     "Lenkep recruitment",
                     "ДПО АЙТИСИТИ",
                     "2дэй академи",
                     "KoksheLab",
                     "Смирнов Алексей Викторович",
                     'Алгоритмика: Красногорск, р-н Павшинская Пойма (ИП Боос Анастасия Александровна)',
                     'Алгоритмика: Салехард (ИП Донгаев Анатолий Михайлович)',
                     'Алгоритмика Челябинск Советский район',
                     'Алгоритмика (ООО Юникод)',
                     'Школа программирования Алгоритмика (ИП Кузьменко Екатерина Александровна)',
                     'Мануспект',
                     'PRO100Robot',
                     'СибГМУ'
                     )

print(len(bad_companies_set))

with open(fullfilepath, "wb") as file:
    pickle.dump(bad_companies_set, file)
