"""Rename column

Revision ID: 5ad430ca23fe
Revises: f891737c3c71
Create Date: 2020-07-25 12:20:17.067370

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '5ad430ca23fe'
down_revision = 'f891737c3c71'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('show', 'start_date', new_column_name='start_time')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('show', 'start_time', new_column_name='start_date')
    # ### end Alembic commands ###
