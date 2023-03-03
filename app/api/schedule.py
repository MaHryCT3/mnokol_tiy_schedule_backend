from fastapi import APIRouter, Depends

from app.api.deps import get_current_year, get_schedule_days_memory, get_tyuiu_api
from app.models.models import CabinetPair, Pair, ScheduleDay, TeacherPair
from app.services.tyuiu.schedule_api import TyuiuScheduleAPI
from app.services.tyuiu.schedule_days_memory import ScheduleDaysMemory

router = APIRouter()


@router.get('/dispatcher/{dispatcher_id}/group/{group_id}', response_model=list[Pair])
async def get_schedule(
    dispatcher_id: str,
    group_id: str,
    *,
    year: int = Depends(get_current_year),
    tyuiu_api: TyuiuScheduleAPI = Depends(get_tyuiu_api),
) -> list[Pair]:
    return await tyuiu_api.get_group_schedule(dispatcher_id, group_id, year)


@router.get('/teacher/{teacher_id}', response_model=list[TeacherPair])
async def get_teacher_schedule(
    teacher_id: str,
    *,
    tyuiu_api: TyuiuScheduleAPI = Depends(get_tyuiu_api),
) -> list[TeacherPair]:
    return await tyuiu_api.get_teacher_schedule(teacher_id)


@router.get('/cabinet/{cabined_id}', response_model=list[CabinetPair])
async def get_cabinets_schedule(
    cabinet_id: int,
    *,
    tyuiu_api: TyuiuScheduleAPI = Depends(get_tyuiu_api),
) -> list[CabinetPair]:
    return await tyuiu_api.get_cabinet_schedule(cabinet_id)


@router.get('/schedule_days', response_model=list[ScheduleDay])
async def get_schedule_days(
    *,
    year: int = Depends(get_current_year),
    schedule_days_memory: ScheduleDaysMemory = Depends(get_schedule_days_memory),
) -> list[ScheduleDay]:
    return await schedule_days_memory.get_schedule_days_from_memory(year)
