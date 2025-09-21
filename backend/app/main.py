from fastapi import FastAPI, APIRouter
from fastapi.staticfiles import StaticFiles
from contextlib import asynccontextmanager
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware
import os

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
    allow_origins=["http://localhost:443","http://localhost:5173","https://ranking.monodev.cloud"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

DIST_DIR = "/app/frontend/dist"

app.mount("/assets", StaticFiles(directory=os.path.join(DIST_DIR, "assets")), name="assets")

@app.get("/", response_class=FileResponse)
def serve_react_index():
    return FileResponse(os.path.join(DIST_DIR, "index.html"))


@app.get("/api/hello")
def hello():
    return {"message": "Hello from API"}
