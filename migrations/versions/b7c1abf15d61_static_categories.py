"""static categories

Revision ID: b7c1abf15d61
Revises: c0998c1815b3
Create Date: 2026-02-04 11:39:45.793454

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "b7c1abf15d61"
down_revision: Union[str, Sequence[str], None] = "c0998c1815b3"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


CATAGORIES = [
    "MEETINGS",
    "EXPENSES",
    "EXPENSES_AS_AGENT",
    "SUBSCRIPTION_AS_AGENT",
    "SUBSCRIPTION",
    "RAFFLE_AS_AGENT",
    "BOOKINGS_AS_AGENT",
    "PUBLICATIONS",
    "ACTIVITIES_AND_EVENTS",
    "FUNDRAISING",
    "BANK_INTEREST",
    "GRANTS_AND_DONATIONS",
    "OTHER",
    "TRANSFER",
    "INSURANCE",
    "DONATIONS",
]


def upgrade() -> None:
    """Upgrade schema."""
    for name in CATAGORIES:
        op.execute(
            sa.text("INSERT INTO categories (name, deleted) VALUES (:name, false)").bindparams(name=name)
        )


def downgrade() -> None:
    """Downgrade schema."""
    for name in CATAGORIES:
        op.execute(
            sa.text("DELETE FROM categories WHERE name = :name").bindparams(name=name)
        )
