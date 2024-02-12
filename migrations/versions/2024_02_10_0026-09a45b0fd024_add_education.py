"""add education

Revision ID: 09a45b0fd024
Revises: 16d28d1a4470
Create Date: 2024-02-10 00:26:06.037309

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from fastapi_storages.integrations.sqlalchemy import FileType
from fastapi_storages import FileSystemStorage

# revision identifiers, used by Alembic.
revision: str = "09a45b0fd024"
down_revision: Union[str, None] = "16d28d1a4470"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


storage = FileSystemStorage(path="static/media/education_section")


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "education_section",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("title", sa.String(length=100), nullable=False),
        sa.Column("description", sa.String(length=5000), nullable=True),
        sa.Column("media1", FileType(storage), nullable=True),
        sa.Column("media2", FileType(storage), nullable=True),
        sa.Column("media3", FileType(storage), nullable=True),
        sa.Column("media4", FileType(storage), nullable=True),
        sa.Column("media5", FileType(storage), nullable=True),
        sa.PrimaryKeyConstraint("id"),
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table("education_section")
    # ### end Alembic commands ###
