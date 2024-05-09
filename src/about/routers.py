from fastapi import APIRouter, status, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi_cache.decorator import cache
from sqlalchemy.orm.exc import NoResultFound

from src.about.models import About
from src.database.database import get_async_session
from src.database.redis import my_key_builder
from src.config import HOUR
from src.exceptions import NO_DATA_FOUND

from .schemas import AboutSchema

about_router = APIRouter(prefix="/about", tags=["About"])


@about_router.get("", response_model=AboutSchema)
@cache(expire=HOUR, key_builder=my_key_builder)
async def get_about(
    session: AsyncSession = Depends(get_async_session),
):
    try:
        record = await session.get(About, 1)
        if not record:
            raise NoResultFound
        return record
    except NoResultFound as exc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=NO_DATA_FOUND
        ) from exc
    except Exception as exc:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(exc)
        )
