from pydantic import parse_obj_as

from app.models.models import (
    Cabinet,
    Group,
    Pair,
    ScheduleDay,
    ScheduleDispatcher,
    Teacher,
    TeacherPair,
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

    async def get_group_schedule(self, dispatcher_id: int, group_id: int, year: int) -> list[Pair]:
        group_schedule_html = await self._get_raw_group_schedule(
            dispatcher_id=dispatcher_id, group_id=group_id, year=year
        )
        pairs = self._parse_group_schedule_html(group_schedule_html)
        return pairs

    async def get_teacher_schedule(self, teacher_id: int):
        dispatchers = await self.get_schedule_dispatchers()
        teacher_schedule_html = await self._get_raw_teacher_schedule(teacher_id, dispatchers)
        teacher_pairs = self._parse_teacher_schedule_html(teacher_schedule_html)

    async def get_schedule_days(self, year: int) -> list[ScheduleDay]:
        frist_group = (await self.get_all_groups())[0]
        first_group_raw_schedule = await self._get_raw_group_schedule(
            dispatcher_id=frist_group.dispatcher_id, group_id=frist_group.id, year=year
        )
        schedule_parser = ScheduleParser(first_group_raw_schedule)
        return schedule_parser.parse_schedule_days()

    async def _get_raw_group_schedule(self, dispatcher_id: int, group_id: int, year: int) -> str:
        params = self._get_group_schedule_params(dispatcher_id, group_id, year)
        return self._get_schedule_html(params)

    async def _get_raw_teacher_schedule(self, teacher_id: int, dispatchers: list[ScheduleDispatcher]) -> list[Pair]:
        params = self._get_teacher_schedule_params(teacher_id, dispatchers)
        return self._get_schedule_html(params)

    async def _get_schedule_html(self, params: dict) -> str:
        response = await self.request_text(self.BASE_LINK + 'shedule/show_shedule.php', params=params)
        return response

    async def _get_data_from_funct_php(self, data: dict) -> dict:
        response = await self.request_json(self.BASE_LINK + 'shedule/funct.php', http_method='POST', data=data)
        return response

    def _parse_group_schedule_html(self, schedule_html: str) -> list[Pair]:
        parser = ScheduleParser(schedule_html)
        return parser.parse_group_schedule()

    def _parse_teacher_schedule_html(self, schedule_html: str) -> list[TeacherPair]:
        parser = ScheduleParser(schedule_html)
        return parser.parse_teacher_schedule()

    def _get_group_schedule_params(self, dispatcher_id: int, group_id: int, year: int) -> str:
        return {
            'action': 'group',
            'union': 0,
            'sid': dispatcher_id,
            'gr': group_id,
            'year': year,
            'vr': 1,
        }

    def _get_teacher_schedule_params(self, teacher_id: int, dispatchers: list[ScheduleDispatcher]):
        dispatchers_params = self._get_dispatchers_params(dispatchers)
        params = {
            'action': 'prep',
            'prep': teacher_id,
            'vr': 1,
            'count': len(dispatchers),
        }
        return params | dispatchers_params

    def _get_dispatchers_params(dispatchers: list[ScheduleDispatcher]) -> dict:
        dispatcher_params = {}
        for i, dispatcher in enumerate(dispatchers):
            dispatcher_params.update(
                {
                    f'shed{i}': int(dispatcher.id),
                    f'union{i}': 0,
                    f'year{i}': dispatcher.year,
                }
            )
        return dispatcher_params

    def __del__(self):
        if not self._session.closed:
            if self._session._connector is not None and self._session._connector_owner:
                self._session._connector._close()
            self._session._connector = None
