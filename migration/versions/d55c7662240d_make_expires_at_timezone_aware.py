"""make expires_at timezone aware

Revision ID: d55c7662240d
Revises: e892d27af3f9
Create Date: 2025-08-14 13:02:25.399928

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'd55c7662240d'
down_revision: Union[str, Sequence[str], None] = 'e892d27af3f9'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.execute(
        "ALTER TABLE sessions "
        "ALTER COLUMN expires_at TYPE TIMESTAMP WITH TIME ZONE "
        "USING expires_at AT TIME ZONE 'UTC';"
    )


def downgrade() -> None:
    op.execute(
        "ALTER TABLE sessions "
        "ALTER COLUMN expires_at TYPE TIMESTAMP WITHOUT TIME ZONE "
        "USING expires_at AT TIME ZONE 'UTC';"
    )
