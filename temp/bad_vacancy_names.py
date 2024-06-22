import pickle
from pathlib import Path

from requests import Session, Response

from secrets.tokens import tokens
from utils.basic_params import workdir

filename = f"bad_vacancy_names.pickle"
fullfilepath = workdir.joinpath(filename)

if Path.exists(fullfilepath):
    with open(fullfilepath, "rb") as file:
        bad_vacancy_names_set = pickle.load(file)
else:
    bad_vacancy_names_set = {"автор", "преподавател", "1c", "php", "репетитор", "учитель"}

print(bad_vacancy_names_set)

with open(fullfilepath, "wb") as file:
    pickle.dump(bad_vacancy_names_set, file)
