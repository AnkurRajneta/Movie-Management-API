"""add column pincode

Revision ID: b6c3548255f3
Revises: 
Create Date: 2025-07-21 11:28:05.281293

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'b6c3548255f3'
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('Films',sa.Column('pincode', sa.String(30)))


def downgrade() -> None:
    op.drop_column('Films','pincode')
