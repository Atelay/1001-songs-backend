from sqlalchemy import String, ForeignKey, Date
from sqlalchemy.orm import relationship, Mapped, mapped_column as mc
from fastapi_storages.integrations.sqlalchemy import FileType
from fastapi_storages import FileSystemStorage

from src.database.database import Base, int_pk, list_array, str_quill


storage = FileSystemStorage(path="static/media/our_projects")


class OurProject(Base):
    __tablename__ = "our_projects"

    id: Mapped[int_pk]
    title: Mapped[str] = mc(String(60))
    short_description: Mapped[str] = mc(String(200))
    preview_photo: Mapped[str] = mc(FileType(storage=storage))
    project_date = mc(Date, nullable=False)
    content: Mapped[str_quill]
    authors: Mapped[list_array]
    editors: Mapped[list_array | None]
    photographers: Mapped[list_array | None]
    city_id: Mapped[int] = mc(ForeignKey("cities.id"))
    location: Mapped["City"] = relationship(back_populates="projects", lazy="selectin")

    def __repr__(self) -> str:
        return f"{self.title}"
