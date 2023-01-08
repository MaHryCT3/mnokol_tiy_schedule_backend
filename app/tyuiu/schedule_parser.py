from typing import TYPE_CHECKING

from bs4 import BeautifulSoup

from app.models.models import Pair, ScheduleDay

if TYPE_CHECKING:
    from bs4.element import Tag


class ScheduleParser:
    """Парсит страницу официального расписания ТИУ"""

    def __init__(self, html: str):
        html_soup = BeautifulSoup(html, 'lxml')
        self._main_table = html_soup.find('table', class_='main_table')

    def parse_schedule_days(self) -> list[ScheduleDay]:
        """Возвращает список дней расписания"""
        week_days_elements = self._get_week_days_elements()
        week_days = self._parse_week_days(week_days_elements)
        return week_days

    def parse_schedule_pairs(self) -> list[Pair]:
        """Возвращает список пар"""
        pairs_elements = self._get_pairs_elements()
        pairs = self._parse_pairs(pairs_elements)
        return pairs

    def _get_week_days_elements(self) -> list['Tag']:
        """Возвращает список элементов с днями недели"""
        return self._main_table.find_all('td', align='center')

    def _parse_week_days(self, week_days_elements: list['Tag']) -> list[ScheduleDay]:
        """Возвращает список дней недели"""
        week_days = []
        for element in week_days_elements:
            week_days.append(self._parse_week_day(element))
        return week_days

    def _parse_week_day(self, week_day_element: 'Tag') -> ScheduleDay:
        """Возвращает день недели"""
        date = week_day_element.next
        day_of_week = date.next.next
        week_type = day_of_week.next.next
        return ScheduleDay(
            date=date,
            day_of_week=day_of_week,
            week_type=week_type,
        )

    def _get_pairs_elements(self) -> list['Tag']:
        """Возвращает список элементов с парами"""
        return self._main_table.find_all('td', class_='urok')

    def _parse_pairs(self, pairs_elements: list['Tag']) -> list[Pair]:
        """Возвращает список пар"""
        pairs = []
        for element in pairs_elements:
            pairs.append(self._parse_pair(element))
        return pairs

    def _parse_pair(self, pair_element: 'Tag') -> Pair:
        """Возвращает пару"""
        name = self._get_pair_name(pair_element)
        teacher = self._get_pair_teacher(pair_element)
        cabinet = self._get_pair_cabinet(pair_element)
        is_replace = self._get_pair_is_replaced(pair_element)
        not_learning = self._get_not_learning(pair_element)
        is_wekeend = self._get_is_weekend(pair_element)
        return Pair(
            name=name,
            teacher=teacher,
            cabinet=cabinet,
            is_replace=is_replace,
            not_learning=not_learning,
            is_weekend=is_wekeend,
        )

    def _get_pair_name(self, pair_element: 'Tag') -> str | None:
        name = pair_element.find('div', class_='disc')
        if not name:
            return ''
        return name.text.strip()

    def _get_pair_teacher(self, pair_element: 'Tag') -> str | None:
        teacher = pair_element.find('div', class_='prep')
        if not teacher:
            return ''
        return teacher.text.strip()

    def _get_pair_cabinet(self, pair_element: 'Tag') -> str | None:
        cabinet = pair_element.find('div', class_='cab')
        if not cabinet:
            return ''
        return cabinet.text.strip()

    def _get_pair_is_replaced(self, pair_element: 'Tag') -> bool:
        return True if pair_element.find('div', class_='zamena') else False

    def _get_not_learning(self, pair_element: 'Tag') -> bool:
        text = pair_element.text.strip()
        if text == 'Не учатся':
            return True
        return False

    def _get_is_weekend(self, pair_element: 'Tag') -> bool:
        text = pair_element.text.strip()
        if text == 'Каникулы':
            return True
        return False
