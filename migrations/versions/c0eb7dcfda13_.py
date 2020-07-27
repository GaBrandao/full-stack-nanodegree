"""Many-to-many relation

Revision ID: c0eb7dcfda13
Revises: d06767bf137a
Create Date: 2020-07-25 10:24:59.004498

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'c0eb7dcfda13'
down_revision = 'd06767bf137a'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('show',
                    sa.Column('id', sa.Integer(), nullable=False),
                    sa.Column('venue_id', sa.Integer(), nullable=True),
                    sa.Column('artist_id', sa.Integer(), nullable=True),
                    sa.Column('starte_date', sa.DateTime(), nullable=False),
                    sa.ForeignKeyConstraint(['artist_id'], ['artist.id'], ),
                    sa.ForeignKeyConstraint(['venue_id'], ['venue.id'], ),
                    sa.PrimaryKeyConstraint('id')
                    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('show')
    # ### end Alembic commands ###
