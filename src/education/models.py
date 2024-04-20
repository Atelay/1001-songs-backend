from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import relationship, Mapped, mapped_column
from fastapi_storages.integrations.sqlalchemy import FileType
from fastapi_storages import FileSystemStorage

from src.database.database import Base, int_pk


storage1 = FileSystemStorage(path="static/media/calendar_and_ritual_categories")
storage2 = FileSystemStorage(path="static/media/song_subcategories")
storage3 = FileSystemStorage(path="static/media/education_page_song_genres")


class EducationPage(Base):
    __tablename__ = "education_page"

    id: Mapped[int_pk]
    title: Mapped[str] = mapped_column(String(60))
    description: Mapped[str] = mapped_column(String(1000))
    recommendations: Mapped[str] = mapped_column(String(10000))
    recommended_sources: Mapped[str] = mapped_column(String(10000))


class CalendarAndRitualCategory(Base):
    __tablename__ = "calendar_and_ritual_categories"

    id: Mapped[int_pk]
    title: Mapped[str] = mapped_column(String(50))
    media: Mapped[str] = mapped_column(FileType(storage=storage1))
    description: Mapped[str] = mapped_column(String(2000))
    recommended_sources: Mapped[str] = mapped_column(String(10000))

    song_subcategories: Mapped[list["SongSubcategory"]] = relationship(
        back_populates="main_category", lazy="selectin"
    )
    education_genres: Mapped[list["EducationPageSongGenre"]] = relationship(
        back_populates="main_category"
    )

    def __repr__(self) -> str:
        return f"{self.title}"


class SongSubcategory(Base):
    __tablename__ = "song_subcategories"

    id: Mapped[int_pk]
    title: Mapped[str] = mapped_column(String(60))
    media: Mapped[str] = mapped_column(FileType(storage=storage2))
    main_category_id: Mapped[int] = mapped_column(
        ForeignKey("calendar_and_ritual_categories.id")
    )

    main_category: Mapped["CalendarAndRitualCategory"] = relationship(
        back_populates="song_subcategories"
    )
    education_genres: Mapped[list["EducationPageSongGenre"]] = relationship(
        back_populates="sub_category", lazy="selectin"
    )

    def __repr__(self) -> str:
        return f"{self.title}"


class EducationPageSongGenre(Base):
    __tablename__ = "education_page_song_genres"

    id: Mapped[int_pk]
    title: Mapped[str] = mapped_column(String(60))
    description: Mapped[str] = mapped_column(String(2000))
    media1: Mapped[str] = mapped_column(FileType(storage=storage3))
    media2: Mapped[str] = mapped_column(FileType(storage=storage3))
    media3: Mapped[str] = mapped_column(FileType(storage=storage3))
    media4: Mapped[str | None] = mapped_column(FileType(storage=storage3))
    media5: Mapped[str | None] = mapped_column(FileType(storage=storage3))
    main_category_id: Mapped[int] = mapped_column(
        ForeignKey("calendar_and_ritual_categories.id")
    )
    sub_category_id: Mapped[int] = mapped_column(ForeignKey("song_subcategories.id"))

    main_category: Mapped["CalendarAndRitualCategory"] = relationship(
        back_populates="education_genres",
        lazy="selectin",
    )
    sub_category: Mapped["SongSubcategory"] = relationship(
        back_populates="education_genres",
        lazy="selectin",
    )
    songs: Mapped[list["Song"]] = relationship(  # type: ignore
        secondary="song_education_genre_association",
        back_populates="education_genres",
        lazy="selectin",
    )

    @property
    def media(self):
        return [self.media1, self.media2, self.media3, self.media4, self.media5]

    def __repr__(self) -> str:
        return f"{self.title}"
