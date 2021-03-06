"""Add UserReadPost model.

Revision ID: 30112ee02e96
Revises: 2bab6c129a79
Create Date: 2015-07-22 12:43:05.902122

"""

# revision identifiers, used by Alembic.
revision = '30112ee02e96'
down_revision = '2bab6c129a79'

from alembic import op
import sqlalchemy as sa


def upgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.create_table('user_read_post',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.Column('post_id', sa.Integer(), nullable=True),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['post_id'], ['post.id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    ### end Alembic commands ###


def downgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('user_read_post')
    ### end Alembic commands ###
