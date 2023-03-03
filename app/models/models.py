from typing import Literal

from pydantic import BaseModel

WeekType = Literal['Четная', 'Нечетная']


class Pair(BaseModel):
    name: str
    teacher: str
    cabinet: str
    is_replace: bool
    not_learning: bool
    is_weekend: bool


class TeacherPair(BaseModel):
    name: str
    group: str
    cabinet: str


class CabinetPair(BaseModel):
    name: str
    group: str
    teacher: str


class ScheduleDay(BaseModel):
    date: str
    day_of_week: str
    week_type: WeekType


class ScheduleDispatcher(BaseModel):
    id: str
    year: str


class Teacher(BaseModel):
    id: str
    name: str


class Cabinet(BaseModel):
    id: str
    number: str
    corps: str
    is_multimedia: bool
    is_computer: bool


class Group(BaseModel):
    id: str
    name: str
    year: str
    base: str
    number: str
    dispatcher_id: str
