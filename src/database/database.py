from typing import AsyncGenerator, Annotated

from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import declarative_base, sessionmaker, mapped_column
from sqlalchemy import ARRAY, String

from src.config import DATABASE_URL


Base = declarative_base()

engine = create_async_engine(DATABASE_URL)
async_session_maker = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)


async def get_async_session() -> AsyncGenerator[AsyncSession, None]:
    async with async_session_maker() as session:
        yield session


int_pk = Annotated[int, mapped_column(primary_key=True)]
str_quill = Annotated[str, mapped_column(String(30000))]
list_array = Annotated[list[str], mapped_column(ARRAY(String(25)))]