from sqlalchemy import Column, String, Date, ForeignKey
from sqlalchemy.orm import relationship, Mapped, mapped_column as mc
from fastapi_storages.integrations.sqlalchemy import FileType
from fastapi_storages import FileSystemStorage

from src.database.database import Base, int_pk, list_array


storage = FileSystemStorage(path="static/media/song")


class Song(Base):
    __tablename__ = "song"

    id: Mapped[int_pk]
    title: Mapped[str] = mc(String(60))
    song_text: Mapped[str | None] = mc(String(5000))
    song_description: Mapped[str | None] = mc(String(300))
    recording_date = Column(Date, nullable=False)
    performers: Mapped[str] = mc(String(200))
    ethnographic_district: Mapped[str] = mc(String(50))
    collectors: Mapped[list_array]
    is_active: Mapped[bool] = mc(default=True)
    video_url: Mapped[str | None] = mc(String(500))
    map_photo: Mapped[str | None] = mc(FileType(storage=storage))
    comment_map: Mapped[str | None] = mc(String(500))
    photo1: Mapped[str | None] = mc(FileType(storage=storage))
    photo2: Mapped[str | None] = mc(FileType(storage=storage))
    photo3: Mapped[str | None] = mc(FileType(storage=storage))
    photo4: Mapped[str | None] = mc(FileType(storage=storage))
    photo5: Mapped[str | None] = mc(FileType(storage=storage))
    ethnographic_photo1: Mapped[str | None] = mc(FileType(storage=storage))
    ethnographic_photo2: Mapped[str | None] = mc(FileType(storage=storage))
    ethnographic_photo3: Mapped[str | None] = mc(FileType(storage=storage))
    ethnographic_photo4: Mapped[str | None] = mc(FileType(storage=storage))
    ethnographic_photo5: Mapped[str | None] = mc(FileType(storage=storage))
    stereo_audio: Mapped[str | None] = mc(FileType(storage=storage))
    multichannel_audio1: Mapped[str | None] = mc(FileType(storage=storage))
    multichannel_audio2: Mapped[str | None] = mc(FileType(storage=storage))
    multichannel_audio3: Mapped[str | None] = mc(FileType(storage=storage))
    multichannel_audio4: Mapped[str | None] = mc(FileType(storage=storage))
    multichannel_audio5: Mapped[str | None] = mc(FileType(storage=storage))
    multichannel_audio6: Mapped[str | None] = mc(FileType(storage=storage))
    fund_id: Mapped[int] = mc(ForeignKey("funds.id"))
    city_id: Mapped[int] = mc(ForeignKey("cities.id"))
    fund = relationship("Fund", back_populates="songs", lazy="selectin")
    city: Mapped["City"] = relationship(back_populates="songs", lazy="selectin")
    education_genres: Mapped[list["EducationPageSongGenre"]] = relationship(
        secondary="song_education_genre_association",
        back_populates="songs",
        lazy="selectin",
    )
    genres: Mapped[list["Genre"]] = relationship(
        secondary="song_genre_association", back_populates="songs", lazy="selectin"
    )

    @property
    def photos(self):
        return [
            self.photo1,
            self.photo2,
            self.photo3,
            self.photo4,
            self.photo5,
        ]

    @property
    def ethnographic_photos(self):
        return [
            self.ethnographic_photo1,
            self.ethnographic_photo2,
            self.ethnographic_photo3,
            self.ethnographic_photo4,
            self.ethnographic_photo5,
        ]

    @property
    def multichannels(self):
        return [
            self.multichannel_audio1,
            self.multichannel_audio2,
            self.multichannel_audio3,
            self.multichannel_audio4,
            self.multichannel_audio5,
            self.multichannel_audio6,
        ]

    def __repr__(self) -> str:
        return f"{self.title}"


class Genre(Base):
    __tablename__ = "genre"

    id: Mapped[int_pk]
    genre_name: Mapped[str] = mc(String(50))
    songs: Mapped[list["Song"]] = relationship(
        secondary="song_genre_association", back_populates="genres", lazy="selectin"
    )

    def __repr__(self) -> str:
        return f"{self.genre_name}"


class SongToGenre(Base):
    __tablename__ = "song_genre_association"

    song_id: Mapped[int] = mc(ForeignKey("song.id"), primary_key=True)
    genre_id: Mapped[int] = mc(ForeignKey("genre.id"), primary_key=True)


class SongToEducationGenre(Base):
    __tablename__ = "song_education_genre_association"

    song_id: Mapped[int] = mc(ForeignKey("song.id"), primary_key=True)
    education_genre_id: Mapped[int] = mc(
        ForeignKey("education_page_song_genres.id"), primary_key=True
    )


class Fund(Base):
    __tablename__ = "funds"

    id: Mapped[int_pk]
    title: Mapped[str] = mc(String(50))
    songs: Mapped[list["Song"]] = relationship(back_populates="fund", lazy="selectin")

    def __repr__(self) -> str:
        return f"{self.title}"
