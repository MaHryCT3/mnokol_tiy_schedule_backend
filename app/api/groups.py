from fastapi import APIRouter, Depends

from app.api.deps import get_tyuiu_api
from app.models.models import Cabinet, Group, Teacher
from app.services.tyuiu.schedule_api import TyuiuScheduleAPI

router = APIRouter()


@router.get('/all', response_model=list[Group])
async def get_all_groups(*, tyuiu_api: TyuiuScheduleAPI = Depends(get_tyuiu_api)) -> list[Group]:
    """Возвращает список всех групп

    **id** - Айди в базе данных\n
    **name** - Название группы\n
    **year** - Год поступления\n
    **base** - База обучения\n
    **number** - Номер группы\n
    """
    return await tyuiu_api.get_all_groups()


@router.get('/all_cabinets', response_model=list[Cabinet])
async def get_all_cabinets(*, tyuiu_api: TyuiuScheduleAPI = Depends(get_tyuiu_api)) -> list[Cabinet]:
    return await tyuiu_api.get_cabinets()


@router.get('/all_teachers', response_model=list[Teacher])
async def get_all_teachers(*, tyuiu_api: TyuiuScheduleAPI = Depends(get_tyuiu_api)) -> list[Teacher]:
    return await tyuiu_api.get_teachers()
