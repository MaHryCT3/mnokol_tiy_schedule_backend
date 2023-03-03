from datetime import datetime

from app.services.tyuiu.schedule_api import TyuiuScheduleAPI
from app.services.tyuiu.schedule_days_memory import ScheduleDaysMemory


def get_current_year() -> int:
    """Возвращает текущий год"""
    return datetime.now().year


async def get_tyuiu_api() -> TyuiuScheduleAPI:
    """Возвращает экземпляр класса TyuiuScheduleAPI"""
    return TyuiuScheduleAPI()


async def get_schedule_days_memory() -> ScheduleDaysMemory:
    """Возвращает экземпляр класса ScheduleDaysMemory"""
    return ScheduleDaysMemory()
