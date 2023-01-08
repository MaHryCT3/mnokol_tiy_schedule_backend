from app.models.models import Cabinet, Group, Teacher


def parse_teachers(data: list[list]) -> list[Teacher]:
    return [Teacher(id=teacher[0], name=teacher[1]) for teacher in data]


def parse_cabinets(data: list[list]) -> list[Cabinet]:
    return [
        Cabinet(
            id=cabinet[0],
            number=cabinet[1],
            corps=cabinet[2],
            is_multimedia=bool(int(cabinet[3])),
            is_computer=bool(int(cabinet[4])),
        )
        for cabinet in data
    ]


def parse_groups(data: list[list], dispatcher_id: str) -> list[Group]:
    return [
        Group(
            id=group[0],
            name=group[1],
            year=group[2],
            base=group[3],
            number=group[4],
            dispatcher_id=dispatcher_id,
        )
        for group in data
    ]
