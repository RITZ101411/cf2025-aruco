from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from sqlalchemy.orm import declarative_base
from dotenv import load_dotenv
from typing import AsyncGenerator
import os

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")

# DB エンジン作成
engine = create_async_engine(DATABASE_URL, echo=True)

# セッションファクトリ作成
async_session = async_sessionmaker(bind=engine, expire_on_commit=False)

# Base クラス
Base = declarative_base()

# セッション取得用 Dependency
async def get_async_session() -> AsyncGenerator[AsyncSession, None]:
    async with async_session() as session:
        yield session
