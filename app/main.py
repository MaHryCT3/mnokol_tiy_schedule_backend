from fastapi import FastAPI

from app.api import api_router
from app.tyuiu.schedule_api import TyuiuScheduleAPI

app = FastAPI()
app.include_router(api_router)

tiuiu_api = TyuiuScheduleAPI()


@app.get('/kst_test')
async def kst_test() -> list[dict]:
    return await tiuiu_api.get_schedule(268, 526, 2023)
