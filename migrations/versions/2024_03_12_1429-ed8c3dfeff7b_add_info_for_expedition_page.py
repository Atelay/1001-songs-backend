"""add info for expedition page

Revision ID: ed8c3dfeff7b
Revises: 6ae94593a10e
Create Date: 2024-03-12 14:29:12.555443

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from fastapi_storages.integrations.sqlalchemy import FileType


# revision identifiers, used by Alembic.
revision: str = "ed8c3dfeff7b"
down_revision: Union[str, None] = "6ae94593a10e"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "expedition_info",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("title", sa.String(length=100), nullable=False),
        sa.Column("description", sa.String(length=500), nullable=True),
        sa.PrimaryKeyConstraint("id"),
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table("expedition_info")
    # ### end Alembic commands ###