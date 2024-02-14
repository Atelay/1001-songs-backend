from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi_pagination import Page
from fastapi_pagination.ext.async_sqlalchemy import paginate
from sqlalchemy.orm.exc import NoResultFound

from src.database.database import get_async_session
from src.exceptions import NO_DATA_FOUND, SERVER_ERROR
from .models import Expedition, ExpeditionCategory
from .schemas import ExpeditionCategorySchema, ExpedListSchema, ExpeditionSchema
from .exceptions import EXPED_NOT_FOUND


expedition_router = APIRouter(prefix="/expedition", tags=["Expedition"])


@expedition_router.get("/categories", response_model=List[ExpeditionCategorySchema])
async def get_all_categories(session: AsyncSession = Depends(get_async_session)):
    """Although the expedition categories are persistent,
    you can use this endpoint to see what identifier each
    category has in the database to later reference other endpoints in the group."""
    try:
        query = select(ExpeditionCategory).order_by("id")
        story = await session.execute(query)
        response = story.scalars().all()
        if not response:
            raise NoResultFound
        return response
    except NoResultFound:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=NO_DATA_FOUND)
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=SERVER_ERROR
        )


@expedition_router.get("/filter", response_model=Page[ExpedListSchema])
async def get_expeditions_list_by_category(
    id: Optional[int] = Query(None), session: AsyncSession = Depends(get_async_session)
):
    """Get expeditions list by category ID."""
    try:
        if id:
            query = select(Expedition).filter(Expedition.category_id == id)
        else:
            query = select(Expedition)
        result = await paginate(session, query)
        if not result.items:
            raise NoResultFound
        return result
    except NoResultFound:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=EXPED_NOT_FOUND
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e)
        )


@expedition_router.get("/{id}", response_model=ExpeditionSchema)
async def get_expedition(id: int, session: AsyncSession = Depends(get_async_session)):
    """Returns detailed information on the expedition by ID."""
    try:
        record = await session.get(Expedition, id)
        if not record:
            raise NoResultFound
        return record
    except NoResultFound:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=EXPED_NOT_FOUND
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e)
        )
