from fastapi import APIRouter, Depends

from app.api.deps import get_current_year, get_tyuiu_api, get_schedule_days_memory
from app.models.models import Pair, ScheduleDay
from app.tyuiu.schedule_api import TyuiuScheduleAPI
from app.tyuiu.schedule_days_memory import ScheduleDaysMemory


router = APIRouter()


@router.get('/dispatcher/{dispatcher_id}/group/{group_id}', response_model=list[Pair])
async def get_schedule(
    dispatcher_id: str,
    group_id: str,
    *,
    year: int = Depends(get_current_year),
    tyuiu_api: TyuiuScheduleAPI = Depends(get_tyuiu_api),
) -> list[Pair]:
    return await tyuiu_api.get_schedule(dispatcher_id, group_id, year)


@router.get('/schedule_days', response_model=list[ScheduleDay])
async def get_schedule_days(
    *,
    year: int = Depends(get_current_year),
    schedule_days_memory: ScheduleDaysMemory = Depends(get_schedule_days_memory),
) -> list[ScheduleDay]:
    return await schedule_days_memory.get_schedule_days_from_memory(year)
