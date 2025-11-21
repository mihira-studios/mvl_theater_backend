"""add project and user access group links

Revision ID: 1f733c0f4811
Revises: 40a732f68a0a
Create Date: 2025-11-19 18:08:25.611158

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '1f733c0f4811'
down_revision: Union[str, Sequence[str], None] = '40a732f68a0a'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass
