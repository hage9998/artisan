from contextlib import asynccontextmanager
from fastapi import FastAPI
from src.database.base import Base
from src.database.session import engine
from src.users.routers import users
from src.messages.routers import messages

app = FastAPI()


@asynccontextmanager
async def app_lifespan(app: FastAPI):
    Base.metadata.create_all(bind=engine)

    yield


app = FastAPI(lifespan=app_lifespan)
app.include_router(users.router)
app.include_router(messages.router)
