from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column as mc
from fastapi_storages.integrations.sqlalchemy import FileType
from fastapi_storages import FileSystemStorage

from src.database.database import Base, int_pk


storage = FileSystemStorage(path="static/media/payment_details")


class PaymentDetails(Base):
    __tablename__ = "payment_details"

    id: Mapped[int_pk]
    organization_name: Mapped[str] = mc(String(75))
    edrpou: Mapped[int]
    bank: Mapped[str] = mc(String(50))
    info: Mapped[str | None] = mc(String(100))
    iban: Mapped[str] = mc(String(34))
    patreon_url: Mapped[str] = mc(String(500))
    coffee_url: Mapped[str] = mc(String(500))
    qr_code_url: Mapped[str] = mc(FileType(storage=storage))
