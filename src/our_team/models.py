from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column as mc
from fastapi_storages.integrations.sqlalchemy import FileType
from fastapi_storages import FileSystemStorage

from src.database.database import Base, int_pk

storage = FileSystemStorage(path="static/media/our_team")


class OurTeam(Base):
    __tablename__ = "our_team"

    id: Mapped[int_pk]
    full_name: Mapped[str] = mc(String(50))
    photo: Mapped[str] = mc(FileType(storage=storage))
    description: Mapped[str] = mc(String(300))

    def __repr__(self) -> str:
        return f"{self.full_name}"
