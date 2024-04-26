from pydantic import BaseModel, Field
from typing import Any
from datetime import date

from typing import TypedDict


class VacancyItem(TypedDict):
    alternate_url: str  # ссылка на вакансию
    apply_alternate_url: str  # ссылка на отклик
    area: dict
    contacts: dict
    experience: dict
    employer: dict
    has_test: bool
    id: int
    name: str
    professional_roles: list
    published_at: str
    response_letter_required: bool
    requirement: str
    salary: dict
    schedule: dict
