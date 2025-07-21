"""add table sales

Revision ID: 40a774a93664
Revises: b6c3548255f3
Create Date: 2025-07-21 12:02:01.409835

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '40a774a93664'
down_revision: Union[str, Sequence[str], None] = 'b6c3548255f3'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table("profit",sa.Column("id", sa.Integer,primary_key=True),
                    sa.Column('Cost', sa.String(30)))


def downgrade() -> None:
    op.drop_table("profit")
