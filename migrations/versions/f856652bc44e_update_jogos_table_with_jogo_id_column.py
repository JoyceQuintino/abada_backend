"""update jogos table with jogo_id column

Revision ID: f856652bc44e
Revises: 30912973207f
Create Date: 2024-04-18 16:27:19.785078

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'f856652bc44e'
down_revision: Union[str, None] = '30912973207f'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('Jogos', sa.Column('jogo_id', sa.Integer(), autoincrement=True, nullable=True))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('Jogos', 'jogo_id')
    # ### end Alembic commands ###