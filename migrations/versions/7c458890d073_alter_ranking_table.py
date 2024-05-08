"""alter Ranking table

Revision ID: 7c458890d073
Revises: 006b002d9f15
Create Date: 2024-04-07 14:32:45.665687

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '7c458890d073'
down_revision: Union[str, None] = '006b002d9f15'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint('Ranking_apelido_key', 'Ranking', type_='unique')
    op.drop_constraint('Ranking_categoria_key', 'Ranking', type_='unique')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_unique_constraint('Ranking_categoria_key', 'Ranking', ['categoria'])
    op.create_unique_constraint('Ranking_apelido_key', 'Ranking', ['apelido'])
    # ### end Alembic commands ###