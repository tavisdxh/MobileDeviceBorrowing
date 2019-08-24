"""empty message

Revision ID: 2a8c8ac2c08a
Revises: aec346d3abd0
Create Date: 2019-08-23 13:55:58.229805

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = '2a8c8ac2c08a'
down_revision = 'aec346d3abd0'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('permission', 'name',
               existing_type=mysql.VARCHAR(length=20),
               nullable=False,
               existing_comment='权限名')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('permission', 'name',
               existing_type=mysql.VARCHAR(length=20),
               nullable=True,
               existing_comment='权限名')
    # ### end Alembic commands ###
