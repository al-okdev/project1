from typing import Union
from contextlib import asynccontextmanager
from vacancies import db
from vacancies.models import Vacancy

from fastapi import FastAPI

@asynccontextmanager
async def lifespan(app: FastAPI):
    await db.init()
    yield

app = FastAPI(lifespan=lifespan)


@app.get("/")
async def read_root():
    await Vacancy.create(experiece="3-6", price="200000", competentions="Django, Linux")
    return {"Hello": "World"}


@app.get("/items/{item_id}")
def read_item(item_id: int, q: Union[str, None] = None):
    return {"item_id": item_id, "q": q}