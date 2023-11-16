import asyncio
import pytest_asyncio
from httpx import AsyncClient

from app.main import app
from app.db import get_db
from app.crud import CRUDForm


@pytest_asyncio.fixture(scope="session")
async def mock_crud_form():
    return CRUDForm()


@pytest_asyncio.fixture(scope="session")
def event_loop():
    policy = asyncio.get_event_loop_policy()
    loop = policy.new_event_loop()
    try:
        yield loop
    finally:
        loop.close()


@pytest_asyncio.fixture(scope="session")
async def get_database():
    async with get_db() as client:
        yield client


@pytest_asyncio.fixture(scope="session")
async def test_client():
    async with AsyncClient(app=app, base_url="http://0.0.0.0:8000") as client:
        yield client
