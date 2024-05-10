from typing import AsyncGenerator
import asyncio

import pytest
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import NullPool
from fastapi.testclient import TestClient

from src.main import app
from src.database.database import get_async_session, Base
from src.config import settings


DATABASE_URL = "postgresql+asyncpg://test_u:test_p@localhost:5777/test_db"

engine = create_async_engine(DATABASE_URL, poolclass=NullPool)
async_session_maker: AsyncSession = sessionmaker(
    engine, class_=AsyncSession, expire_on_commit=False
)
Base.metadata.bind = engine


async def override_get_async_session() -> AsyncGenerator[AsyncSession, None]:
    async with async_session_maker() as session:
        yield session


app.dependency_overrides[get_async_session] = override_get_async_session
client = TestClient(app)


@pytest.fixture(autouse=True, scope="session")
async def prepare_database():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)


@pytest.fixture(scope="session")
def event_loop(request):
    """Create an instance of the default event loop for each test case."""
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest.fixture(scope="session")
async def ac() -> AsyncGenerator[AsyncClient, None]:
    async with AsyncClient(app=app, base_url=settings.BASE_URL) as ac:
        yield ac
