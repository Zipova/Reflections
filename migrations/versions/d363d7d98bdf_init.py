"""Init

Revision ID: d363d7d98bdf
Revises: 036235d3942d
Create Date: 2023-07-31 13:27:37.884405

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'd363d7d98bdf'
down_revision = '036235d3942d'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('users', sa.Column('about', sa.String(length=255), nullable=True))
    op.add_column('users', sa.Column('birthday', sa.String(length=20), nullable=True))
    op.add_column('users', sa.Column('country', sa.String(length=50), nullable=True))
    op.add_column('users', sa.Column('phone', sa.String(length=20), nullable=True))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('users', 'phone')
    op.drop_column('users', 'country')
    op.drop_column('users', 'birthday')
    op.drop_column('users', 'about')
    # ### end Alembic commands ###
