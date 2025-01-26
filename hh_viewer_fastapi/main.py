from typing import Union
from contextlib import asynccontextmanager
import db
from vacancies.models import Vacancy
from vacancies.admin import VacancyAdmin
from users.models import User
from users.admin import UserAdmin

from fastadmin import fastapi_app as admin_app

from fastapi import FastAPI

@asynccontextmanager
async def lifespan(app: FastAPI):
    await db.init()
    yield

app = FastAPI(lifespan=lifespan)
app.mount("/admin", admin_app)
    
@app.get("/")
async def read_root():
    await Vacancy.create(experiece="3-6", price="200000", competentions="Django, Linux")
    return {"Hello": "World"}


@app.get("/items/{item_id}")
def read_item(item_id: int, q: Union[str, None] = None):
    return {"item_id": item_id, "q": q}