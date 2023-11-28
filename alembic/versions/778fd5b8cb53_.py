"""empty message

Revision ID: 778fd5b8cb53
Revises: 10ce5e5a1b09
Create Date: 2023-11-28 18:13:05.873642

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '778fd5b8cb53'
down_revision: Union[str, None] = '10ce5e5a1b09'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('users', sa.Column('is_active', sa.BOOLEAN(), nullable=True))
    op.add_column('users', sa.Column('is_staff', sa.BOOLEAN(), nullable=True))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('users', 'is_staff')
    op.drop_column('users', 'is_active')
    # ### end Alembic commands ###
