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

app.mount("/static", StaticFiles(directory="static"), name="static")
env = Environment(loader=FileSystemLoader("./templates"))

app.include_router(system.router, tags=["system"])

router = APIRouter()

@router.get("/", response_class=HTMLResponse)
async def index():
    template = env.get_template("index.html")
    data = "This is Data"
    html_content = template.render(embed_data=data)
    return html_content

app.include_router(router)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:8000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)