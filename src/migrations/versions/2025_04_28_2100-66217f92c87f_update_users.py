"""Update Users

Revision ID: 66217f92c87f
Revises: 2384d3697721
Create Date: 2025-04-28 21:00:16.466804

"""

from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision: str = "66217f92c87f"
down_revision: Union[str, None] = "2384d3697721"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column(
        "users", sa.Column("first_name", sa.String(length=100), nullable=False)
    )
    op.add_column(
        "users", sa.Column("last_name", sa.String(length=100), nullable=False)
    )


def downgrade() -> None:
    op.drop_column("users", "last_name")
    op.drop_column("users", "first_name")
