"""Update Users 2

Revision ID: 2c047d5823e9
Revises: 66217f92c87f
Create Date: 2025-04-28 21:11:41.630207

"""

from typing import Sequence, Union

from alembic import op

# revision identifiers, used by Alembic.
revision: str = "2c047d5823e9"
down_revision: Union[str, None] = "66217f92c87f"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_unique_constraint(None, "users", ["email"])


def downgrade() -> None:
    op.drop_constraint(None, "users", type_="unique")
