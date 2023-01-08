from fastapi import APIRouter, Depends

from app.api.deps import get_tyuiu_api
from app.models.models import Group
from app.tyuiu.schedule_api import TyuiuScheduleAPI


router = APIRouter()


@router.get('/all', response_model=list[Group])
async def get_all_groups(tyuiu_api: TyuiuScheduleAPI = Depends(get_tyuiu_api)) -> list[Group]:
    """Возвращает список всех групп

    **id** - Айди в базе данных\n
    **name** - Название группы\n
    **year** - Год поступления\n
    **base** - База обучения\n
    **number** - Номер группы\n
    """
    return await tyuiu_api.get_all_groups()
