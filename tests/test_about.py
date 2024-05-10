import pytest
from httpx import AsyncClient
from fastapi import status
from contextlib import nullcontext as does_not_raise

from scripts.fake_data import FAKE_ABOUT
from src.about.models import About
from src.about.schemas import AboutSchema
from .conftest import async_session_maker


LONG_CONTENT = "*" * (About.content.type.length + 1)
LONG_TITLE = "*" * (About.title.type.length + 1)


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


@pytest.mark.parametrize(
    "id, title, content, expectation",
    [
        (1, "test", LONG_CONTENT, pytest.raises(ValueError)),
        (1, LONG_TITLE, "Test content", pytest.raises(ValueError)),
        (0, "test", "Test content", pytest.raises(ValueError)),
        (1, 123, "Test content", pytest.raises(ValueError)),
        (1, "test", 123, pytest.raises(ValueError)),
        (1, "test", "Test content", does_not_raise()),
    ],
)
def test_about_schema(id, title, content, expectation):
    with expectation:
        AboutSchema(id=id, title=title, content=content)
