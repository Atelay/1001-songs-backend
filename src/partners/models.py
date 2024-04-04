from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column as mc
from fastapi_storages.integrations.sqlalchemy import FileType
from fastapi_storages import FileSystemStorage

from src.database.database import Base, int_pk

storage = FileSystemStorage(path="static/media/partners")


class Partners(Base):
    __tablename__ = "partners"

    id: Mapped[int_pk]
    photo: Mapped[str] = mc(FileType(storage=storage))
    link: Mapped[str | None] = mc(String(500))

    def __repr__(self) -> str:
        return f"{self.link}"
