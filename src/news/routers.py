from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException, status, Query
from fastapi_pagination import Page
from fastapi_pagination.ext.async_sqlalchemy import paginate
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm.exc import NoResultFound
from fastapi_cache.decorator import cache

from src.config import DAY, HOUR
from src.database.database import get_async_session
from src.database.redis import my_key_builder
from src.exceptions import NO_DATA_FOUND, SERVER_ERROR
from .exceptions import NO_NEWS_FOUND
from .service import get_records
from .models import NewsCategory, News
from .schemas import NewsSchema, NewCategorySchema, NewsSchemaList


news_router = APIRouter(prefix="/news", tags=["News"])


@news_router.get("/categories", response_model=List[NewCategorySchema])
@cache(expire=DAY, key_builder=my_key_builder)
async def get_categories(session: AsyncSession = Depends(get_async_session)):
    return await get_records(NewsCategory, session)


@news_router.get("", response_model=Page[NewsSchemaList])
@cache(expire=HOUR, key_builder=my_key_builder)
async def get_news(
    category_id: int = Query(
        None, description="Press the button to add a field for a new ID"
    ),
    news_exclude: Optional[int] = Query(None),
    session: AsyncSession = Depends(get_async_session),
):
    """
    Use this endpoint to retrieve news. You can filter them by category by passing one or more **category `ID`s**.
    """
    try:
        query = select(News).order_by(News.created_at.desc())
        if category_id:
            query = query.filter(News.category_id == category_id)
        if news_exclude:
            query = query.filter(News.id != news_exclude)
        result = await paginate(session, query)
        if not result.items:
            raise NoResultFound
        return result

    except NoResultFound as exc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=NO_NEWS_FOUND,
        ) from exc
    except Exception as exc:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(exc)
        )


@news_router.get("/{id}", response_model=NewsSchema)
@cache(expire=HOUR, key_builder=my_key_builder)
async def get_one_news(id: int, session: AsyncSession = Depends(get_async_session)):
    try:
        record = await session.get(News, id)
        if not record:
            raise NoResultFound
        return record
    except NoResultFound as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=NO_DATA_FOUND) from exc
    except Exception as exc:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=SERVER_ERROR
        ) from exc
