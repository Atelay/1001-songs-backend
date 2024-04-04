from datetime import datetime

from fastapi_storages import FileSystemStorage
from sqlalchemy import Column, String, ForeignKey, Date
from sqlalchemy.orm import relationship, Mapped, mapped_column
from fastapi_storages.integrations.sqlalchemy import FileType

from src.database.database import Base, int_pk, str_quill, list_array


storage = FileSystemStorage(path="static/media/news")


class NewsCategory(Base):
    __tablename__ = "news_category"

    id: Mapped[int_pk]
    name: Mapped[str] = mapped_column(String(100))
    news: Mapped[list["News"]] = relationship(back_populates="category")

    def __repr__(self) -> str:
        return f"{self.name}"


class News(Base):
    __tablename__ = "news"

    id: Mapped[int_pk]
    title: Mapped[str] = mapped_column(String(60))
    content: Mapped[str_quill]
    short_description: Mapped[str] = mapped_column(String(200))
    authors: Mapped[list_array]
    editors: Mapped[list_array | None]
    photographers: Mapped[list_array | None]
    preview_photo: Mapped[str] = mapped_column(FileType(storage=storage))
    created_at: datetime = Column(Date, nullable=False)
    category_id: Mapped[int] = mapped_column(ForeignKey("news_category.id"))
    city_id: Mapped[int] = mapped_column(ForeignKey("cities.id"))
    category: Mapped["NewsCategory"] = relationship(
        back_populates="news", lazy="selectin"
    )
    location: Mapped["City"] = relationship(back_populates="news", lazy="selectin")

    def __repr__(self) -> str:
        return f"{self.title}"
