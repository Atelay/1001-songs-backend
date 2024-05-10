import pytest
from httpx import AsyncClient
from fastapi import status

from scripts.fake_data import FAKE_ABOUT
from src.about.models import About
from .conftest import async_session_maker


@pytest.mark.asyncio
async def test_get_about(ac: AsyncClient):
    response = await ac.get("api/v1/about")
    assert response.json()["detail"] == "No data found."
    assert response.status_code == status.HTTP_404_NOT_FOUND

    async with async_session_maker() as session:
        session.add(About(**FAKE_ABOUT))
        await session.commit()

    response = await ac.get("api/v1/about")
    data: dict = response.json()
    assert response.status_code == status.HTTP_200_OK
    assert data["content"] == FAKE_ABOUT["content"]
    assert data["title"] == FAKE_ABOUT["title"]
    assert data["id"] == 1
