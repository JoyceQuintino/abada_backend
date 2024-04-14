"""add fase column in  Ranking table

Revision ID: 58d6e3c67398
Revises: 0b665db99efa
Create Date: 2024-04-07 14:14:02.832341

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '58d6e3c67398'
down_revision: Union[str, None] = '0b665db99efa'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('Ranking', sa.Column('fase', sa.Integer(), nullable=False))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('Ranking', 'fase')
    # ### end Alembic commands ###
