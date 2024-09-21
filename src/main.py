from contextlib import asynccontextmanager
from fastapi import FastAPI
from src.database.base import Base
from src.database.session import engine
from .users.routers import users


app = FastAPI()


@asynccontextmanager
async def app_lifespan(app: FastAPI):
    Base.metadata.create_all(bind=engine)

    yield


app = FastAPI(lifespan=app_lifespan)
app.include_router(users.router)
