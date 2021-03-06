"""Add need_analysis to Post.

Revision ID: 2ba2d5ae54cc
Revises: 4c281030504f
Create Date: 2014-11-28 15:38:40.153081

"""

# revision identifiers, used by Alembic.
revision = '2ba2d5ae54cc'
down_revision = '4c281030504f'

from alembic import op
import sqlalchemy as sa


def upgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.add_column('post', sa.Column('need_analysis', sa.Boolean(), nullable=True))
    ### end Alembic commands ###


def downgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('post', 'need_analysis')
    ### end Alembic commands ###
