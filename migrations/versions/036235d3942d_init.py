"""Init

Revision ID: 036235d3942d
Revises: 38334c70a979
Create Date: 2023-07-30 18:05:35.231973

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '036235d3942d'
down_revision = '38334c70a979'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('rate',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('photo_id', sa.Integer(), nullable=True),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.Column('rate', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['photo_id'], ['photos.id'], ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id')
    )
    op.add_column('photos', sa.Column('rated_by', sa.ARRAY(sa.Integer()), nullable=True))
    op.add_column('photos', sa.Column('average_rating', sa.Float(), nullable=True))
    op.drop_column('photos', 'rating')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('photos', sa.Column('rating', sa.DOUBLE_PRECISION(precision=53), autoincrement=False, nullable=True))
    op.drop_column('photos', 'average_rating')
    op.drop_column('photos', 'rated_by')
    op.drop_table('rate')
    # ### end Alembic commands ###
