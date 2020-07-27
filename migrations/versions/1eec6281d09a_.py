"""Initial database models

Revision ID: 1eec6281d09a
Revises: 
Create Date: 2020-07-24 14:04:41.765210

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '1eec6281d09a'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('Artist',
                    sa.Column('id', sa.Integer(), nullable=False),
                    sa.Column('name', sa.String(), nullable=False),
                    sa.Column('city', sa.String(length=120), nullable=False),
                    sa.Column('state', sa.String(length=120), nullable=False),
                    sa.Column('phone', sa.String(length=120), nullable=True),
                    sa.Column('genres', sa.String(length=120), nullable=True),
                    sa.Column('image_link', sa.String(
                        length=500), nullable=True),
                    sa.Column('facebook_link', sa.String(
                        length=120), nullable=True),
                    sa.PrimaryKeyConstraint('id')
                    )
    op.create_table('Venue',
                    sa.Column('id', sa.Integer(), nullable=False),
                    sa.Column('name', sa.String(), nullable=False),
                    sa.Column('city', sa.String(length=120), nullable=False),
                    sa.Column('state', sa.String(length=120), nullable=False),
                    sa.Column('address', sa.String(
                        length=120), nullable=False),
                    sa.Column('phone', sa.String(length=120), nullable=True),
                    sa.Column('image_link', sa.String(
                        length=500), nullable=True),
                    sa.Column('facebook_link', sa.String(
                        length=120), nullable=True),
                    sa.PrimaryKeyConstraint('id')
                    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('Venue')
    op.drop_table('Artist')
    # ### end Alembic commands ###
