from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column

from src.database.database import Base, str_quill, int_pk


class About(Base):
    __tablename__ = "about"

    id: Mapped[int_pk]
    title: Mapped[str] = mapped_column(String(60))
    content: Mapped[str_quill]
