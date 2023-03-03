from datetime import datetime, timedelta, timezone

from loguru import logger

from app.models import ScheduleDay
from app.services.tyuiu.schedule_api import TyuiuScheduleAPI
from app.utils import singleton

tuymen_timezone = timezone(offset=timedelta(hours=5))


@singleton
class ScheduleDaysMemory:
    def __init__(self):
        self._schedule_days: list[ScheduleDay] = None
        self._last_update: datetime = None
        self._schedule_api = TyuiuScheduleAPI()

    async def get_schedule_days_from_memory(self, year: int) -> list[ScheduleDay]:
        logger.debug(
            'In get_schedule_days and schedule_days = {}, last_update = {}', self._schedule_days, self._last_update
        )
        if self._schedule_days is None:
            await self.update_schedule_days(year)
        elif self.check_last_update_expire():
            await self.update_schedule_days(year)
        return self._schedule_days

    async def update_schedule_days(self, year: int) -> None:
        self._schedule_days = await self._schedule_api.get_schedule_days(year)
        self._last_update = datetime.now(tuymen_timezone)

    def check_last_update_expire(self) -> bool:
        if self._last_update is None:
            return True
        now = datetime.now(tuymen_timezone)
        if self._last_update.day != now.day:
            return True
        if self._last_update.month != now.month:
            return True
        return False
