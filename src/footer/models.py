from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column
from fastapi_storages.integrations.sqlalchemy import FileType
from fastapi_storages import FileSystemStorage

from src.database.database import Base, int_pk


storage = FileSystemStorage(path="static/media/footer")


class Footer(Base):
    __tablename__ = "footer"

    id: Mapped[int_pk]
    reporting: Mapped[str] = mapped_column(FileType(storage=storage))
    privacy_policy: Mapped[str] = mapped_column(FileType(storage=storage))
    rules_and_terms: Mapped[str] = mapped_column(FileType(storage=storage))
    email: Mapped[str] = mapped_column(String(30))
    facebook_url: Mapped[str | None] = mapped_column(String(500))
    youtube_url: Mapped[str | None] = mapped_column(String(500))
