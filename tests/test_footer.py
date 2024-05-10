from pydantic import ValidationError
import pytest
from httpx import AsyncClient
from fastapi import status
from contextlib import nullcontext as does_not_raise

from scripts.fake_data import FAKE_FOOTER
from src.footer.models import Footer
from src.footer.schemas import FooterSchema
from src.config import settings
from .conftest import async_session_maker


@pytest.mark.asyncio
async def test_get_footer(ac: AsyncClient):
    response = await ac.get("api/v1/footer")
    assert response.json()["detail"] == "No data found."
    assert response.status_code == status.HTTP_404_NOT_FOUND

    async with async_session_maker() as session:
        session.add(Footer(**FAKE_FOOTER))
        await session.commit()

    response = await ac.get("api/v1/footer")
    data: dict = response.json()
    assert response.status_code == status.HTTP_200_OK
    assert len(data) == len(FAKE_FOOTER)
    assert data["email"] == FAKE_FOOTER["email"]
    assert data["facebook_url"] == FAKE_FOOTER["facebook_url"]
    assert data["youtube_url"] == FAKE_FOOTER["youtube_url"]


class TestFooterSchema:
    @pytest.mark.parametrize(
        "reporting, privacy_policy, rules_and_terms, email, facebook_url, youtube_url, expectation",
        [
            ("http://example.com", None, None, None, None, None, does_not_raise()),
            (None, "http://example.com", None, None, None, None, does_not_raise()),
            (None, None, "http://example.com", None, None, None, does_not_raise()),
            (None, None, None, "Djohny@example.com", None, None, does_not_raise()),
            (None, None, None, None, "http://example.com", None, does_not_raise()),
            (None, None, None, None, None, "http://example.com", does_not_raise()),
            (None, None, None, "invalid", None, None, pytest.raises(ValidationError)),
            (None, None, None, None, "invalid", None, pytest.raises(ValidationError)),
            (None, None, None, None, None, "invalid", pytest.raises(ValidationError)),
        ],
    )
    def test_footer_schema_with_params(
        self,
        reporting,
        privacy_policy,
        rules_and_terms,
        email,
        facebook_url,
        youtube_url,
        expectation,
    ):
        with expectation:
            FooterSchema(
                reporting=reporting,
                privacy_policy=privacy_policy,
                rules_and_terms=rules_and_terms,
                email=email,
                facebook_url=facebook_url,
                youtube_url=youtube_url,
            )

    def test_add_base_url(self):
        result = FooterSchema.add_base_url("reporting_path", None)
        assert result == f"{settings.BASE_URL}/reporting_path"
