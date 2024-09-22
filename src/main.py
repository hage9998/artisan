from contextlib import asynccontextmanager
from fastapi import FastAPI
from src.database.base import Base
from src.database.session import engine
from src.users.routers import users
from src.messages.routers import messages
from src.auth.routers import auth
from fastapi.middleware.cors import CORSMiddleware


@asynccontextmanager
async def app_lifespan(app: FastAPI):
    Base.metadata.create_all(bind=engine)

    yield


app = FastAPI(lifespan=app_lifespan)

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE"],
    allow_headers=["*"],
)


app.include_router(users.router)
app.include_router(messages.router)
app.include_router(auth.router)
