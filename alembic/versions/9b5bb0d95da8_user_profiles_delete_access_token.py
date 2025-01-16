"""user_profiles_delete_access_token

Revision ID: 9b5bb0d95da8
Revises: 04ffa7ece6f4
Create Date: 2025-01-15 20:10:08.959016

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '9b5bb0d95da8'
down_revision: Union[str, None] = '04ffa7ece6f4'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint('user_profiles_access_token_key', 'user_profiles', type_='unique')
    op.drop_column('user_profiles', 'access_token')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('user_profiles', sa.Column('access_token', sa.VARCHAR(), autoincrement=False, nullable=True))
    op.create_unique_constraint('user_profiles_access_token_key', 'user_profiles', ['access_token'])
    # ### end Alembic commands ###