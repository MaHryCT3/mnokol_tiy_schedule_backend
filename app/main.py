from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api import api_router
from app.services.tyuiu.schedule_api import TyuiuScheduleAPI

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_methods=['*'],
    allow_headers=['*'],
)
app.include_router(api_router)


tiuiu_api = TyuiuScheduleAPI()
