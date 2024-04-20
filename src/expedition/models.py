from sqlalchemy import Column, String, ForeignKey, Integer, Date, ARRAY
from sqlalchemy.orm import relationship, Mapped, mapped_column
from fastapi_storages.integrations.sqlalchemy import FileType
from fastapi_storages import FileSystemStorage

from src.database.database import Base, int_pk, str_quill


storage = FileSystemStorage(path="static/media/expedition")


class ExpeditionCategory(Base):
    __tablename__ = "expedition_category"

    id: Mapped[int_pk]
    title: Mapped[str] = mapped_column(String(30))
    expeditions: Mapped["Expedition"] = relationship(
        back_populates="category", lazy="selectin"
    )

    def __repr__(self) -> str:
        return f"{self.title}"


class ExpeditionInfo(Base):
    __tablename__ = "expedition_info"

    id: Mapped[int_pk]
    title: Mapped[str] = mapped_column(String(60))
    description: Mapped[str] = mapped_column(String(600))


class Expedition(Base):
    __tablename__ = "expedition"

    id: Mapped[int_pk]
    title: Mapped[str] = mapped_column(String(60), index=True)
    short_description: Mapped[str] = mapped_column(String(200), index=True)
    map_photo: Mapped[str] = mapped_column(FileType(storage=storage))
    preview_photo: Mapped[str] = mapped_column(FileType(storage=storage))
    expedition_date = Column(Date, nullable=False)
    content: Mapped[str_quill]
    category_id: Mapped[int] = mapped_column(ForeignKey("expedition_category.id"))
    category: Mapped["ExpeditionCategory"] = relationship(
        back_populates="expeditions", lazy="selectin"
    )

    city_id: Mapped[int] = mapped_column(ForeignKey("cities.id"))
    location: Mapped["City"] = relationship(
        back_populates="expeditions", lazy="selectin"
    )

    authors: Mapped[list[str]] = mapped_column(ARRAY(String(100)))
    editors: Mapped[list[str] | None] = mapped_column(ARRAY(String(100)))
    photographers: Mapped[list[str] | None] = mapped_column(ARRAY(String(100)))
    recording: Mapped[list[str] | None] = mapped_column(ARRAY(String(100)))

    def __repr__(self) -> str:
        return f"{self.title}"
