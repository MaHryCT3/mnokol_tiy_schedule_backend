from fastapi import APIRouter

from app.api import groups, schedule

api_router = APIRouter(prefix='/api/v1')
api_router.include_router(groups.router, prefix='/groups')
api_router.include_router(schedule.router, prefix='/schedule')
