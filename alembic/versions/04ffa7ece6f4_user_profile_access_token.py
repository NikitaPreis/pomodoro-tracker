"""user_profile_access_token

Revision ID: 04ffa7ece6f4
Revises: fdaccba3f8eb
Create Date: 2025-01-15 18:28:20.325837

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '04ffa7ece6f4'
down_revision: Union[str, None] = 'fdaccba3f8eb'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('user_profiles', 'access_token',
               existing_type=sa.VARCHAR(),
               nullable=True)
    op.create_unique_constraint(None, 'user_profiles', ['password'])
    op.create_unique_constraint(None, 'user_profiles', ['username'])
    op.create_unique_constraint(None, 'user_profiles', ['id'])
    op.create_unique_constraint(None, 'user_profiles', ['access_token'])
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'user_profiles', type_='unique')
    op.drop_constraint(None, 'user_profiles', type_='unique')
    op.drop_constraint(None, 'user_profiles', type_='unique')
    op.drop_constraint(None, 'user_profiles', type_='unique')
    op.alter_column('user_profiles', 'access_token',
               existing_type=sa.VARCHAR(),
               nullable=False)
    # ### end Alembic commands ###
