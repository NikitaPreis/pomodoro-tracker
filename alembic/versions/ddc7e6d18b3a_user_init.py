"""user_init

Revision ID: ddc7e6d18b3a
Revises: 5b06ec6b02e2
Create Date: 2025-02-21 19:26:44.458568

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'ddc7e6d18b3a'
down_revision: Union[str, None] = '5b06ec6b02e2'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    pass
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    pass
    # ### end Alembic commands ###
