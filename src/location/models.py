from fastapi_storages import FileSystemStorage
from sqlalchemy import String, ForeignKey
from sqlalchemy.orm import relationship, Mapped, mapped_column
from fastapi_storages.integrations.sqlalchemy import FileType

from src.database.database import Base, int_pk


storage = FileSystemStorage(path="static/media/cities")


class Country(Base):
    __tablename__ = "countries"

    id: Mapped[int_pk]
    name: Mapped[str] = mapped_column(String(50))
    regions: Mapped[list["Region"]] = relationship(
        back_populates="country", lazy="selectin"
    )
    cities: Mapped[list["City"]] = relationship(back_populates="country")

    def __repr__(self) -> str:
        return f"{self.name}"


class Region(Base):
    __tablename__ = "regions"

    id: Mapped[int_pk]
    name: Mapped[str] = mapped_column(String(50))
    country_id: Mapped[int] = mapped_column(ForeignKey("countries.id"))
    country: Mapped["Country"] = relationship(back_populates="regions")
    cities: Mapped[list["City"]] = relationship(
        back_populates="region", lazy="selectin"
    )

    def __repr__(self) -> str:
        return f"{self.name}"


class City(Base):
    __tablename__ = "cities"

    id: Mapped[int_pk]
    name: Mapped[str] = mapped_column(String(50))
    latitude: Mapped[float]
    longitude: Mapped[float]
    administrative_code: Mapped[str] = mapped_column(String(50), unique=True)
    photo: Mapped[str | None] = mapped_column(FileType(storage=storage))
    region_id: Mapped[int] = mapped_column(ForeignKey("regions.id"))
    country_id: Mapped[int] = mapped_column(ForeignKey("countries.id"))

    region: Mapped["Region"] = relationship(back_populates="cities", lazy="selectin")
    country: Mapped["Country"] = relationship(back_populates="cities", lazy="selectin")
    songs: Mapped[list["Song"]] = relationship(back_populates="city", lazy="selectin")
    expeditions: Mapped[list["Expedition"]] = relationship(
        back_populates="location", lazy="selectin"
    )
    projects: Mapped[list["OurProject"]] = relationship(
        back_populates="location", lazy="selectin"
    )
    news: Mapped[list["News"]] = relationship(
        back_populates="location", lazy="selectin"
    )

    def __repr__(self) -> str:
        return f"{self.name}, {self.region}, {self.administrative_code}"
