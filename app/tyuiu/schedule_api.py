from pydantic import parse_obj_as

from app.models.models import (
    Cabinet,
    Group,
    Pair,
    ScheduleDay,
    ScheduleDispatcher,
    Teacher,
)
from app.models.models_parser import parse_cabinets, parse_groups, parse_teachers
from app.tyuiu.schedule_parser import ScheduleParser
from app.tyuiu.http_client import HTTPClient


class TyuiuScheduleAPI(HTTPClient):
    BASE_LINK: str = 'http://mnokol.tyuiu.ru/rtsp/'

    async def get_all_groups(self) -> list[Group]:
        dispatchers = await self.get_schedule_dispatchers()
        dispatcher_ids = [diaptacher.id for diaptacher in dispatchers]
        groups = []
        for dispatcher_id in dispatcher_ids:
            groups += await self.get_groups_by_dispatcher(dispatcher_id)
        return groups

    async def get_groups_by_dispatcher(self, dispatcher_id: str) -> list[Group]:
        data = {
            'action': 'load',
            'act': 'list_groups',
            'otd': '0',
            'vd': dispatcher_id,
        }
        response_data = await self._get_data_from_funct_php(data)
        return parse_groups(response_data, dispatcher_id)

    async def get_schedule_dispatchers(self) -> list[ScheduleDispatcher]:
        data = {
            'action': 'load_info',
        }
        response_data = await self._get_data_from_funct_php(data)
        return parse_obj_as(list[ScheduleDispatcher], response_data)

    async def get_teachers(self) -> list[Teacher]:
        data = {
            'action': 'load',
            'act': 'list_prepods',
            'otd': '0',
            'bs': '0',
        }
        response_data = await self._get_data_from_funct_php(data)
        return parse_teachers(response_data)

    async def get_cabinets(self) -> list[Cabinet]:
        data = {
            'action': 'load',
            'act': 'cabs',
            'otd': '0',
            'bs': '0',
        }
        response_data = await self._get_data_from_funct_php(data)
        return parse_cabinets(response_data)

    async def get_schedule(self, dispatcher_id: int, group_id: int, year: int) -> list[Pair]:
        response = await self._get_raw_schedule(dispatcher_id=dispatcher_id, group_id=group_id, year=year)
        pairs = self._parse_schedule(response)
        return pairs

    async def get_schedule_days(self, year: int) -> list[ScheduleDay]:
        frist_group = (await self.get_all_groups())[0]
        first_group_raw_schedule = await self._get_raw_schedule(
            dispatcher_id=frist_group.dispatcher_id, group_id=frist_group.id, year=year
        )
        schedule_parser = ScheduleParser(first_group_raw_schedule)
        return schedule_parser.parse_schedule_days()

    async def _get_raw_schedule(self, dispatcher_id: int, group_id: int, year: int) -> str:
        params = {
            'action': 'group',
            'union': 0,
            'sid': dispatcher_id,
            'gr': group_id,
            'year': year,
            'vr': 1,
        }
        response = await self.request_text(self.BASE_LINK + 'shedule/show_shedule.php', params=params)
        return response

    async def _get_data_from_funct_php(self, data: dict) -> dict:
        response = await self.request_json(self.BASE_LINK + 'shedule/funct.php', http_method='POST', data=data)
        return response

    def _parse_schedule(self, schedule_html: str) -> list[Pair]:
        parser = ScheduleParser(schedule_html)
        return parser.parse_schedule_pairs()

    def __del__(self):
        if not self._session.closed:
            if self._session._connector is not None and self._session._connector_owner:
                self._session._connector._close()
            self._session._connector = None
