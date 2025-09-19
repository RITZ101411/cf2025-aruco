from fastapi import FastAPI, APIRouter
from fastapi.staticfiles import StaticFiles
from contextlib import asynccontextmanager
from fastapi.responses import HTMLResponse
from jinja2 import Environment, FileSystemLoader
from fastapi.middleware.cors import CORSMiddleware

from db.session import engine
from db.base import Base
from routers import system

@asynccontextmanager
async def lifespan(app: FastAPI):
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield

app = FastAPI(lifespan=lifespan)


app.include_router(system.router, tags=["system"])

router = APIRouter()

app.include_router(router)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:8000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)