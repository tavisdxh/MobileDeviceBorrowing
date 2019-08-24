"""empty message

Revision ID: 2b4355d4395f
Revises: 2a8c8ac2c08a
Create Date: 2019-08-23 14:00:12.301085

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = '2b4355d4395f'
down_revision = '2a8c8ac2c08a'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('permission', 'desc',
               existing_type=mysql.VARCHAR(length=20),
               type_=sa.String(length=50),
               existing_comment='描述',
               existing_nullable=True)
    op.alter_column('role', 'desc',
               existing_type=mysql.VARCHAR(length=20),
               type_=sa.String(length=50),
               existing_comment='描述',
               existing_nullable=True)
    op.alter_column('user', 'email',
               existing_type=mysql.VARCHAR(length=100),
               type_=sa.String(length=40),
               existing_comment='邮箱',
               existing_nullable=False)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('user', 'email',
               existing_type=sa.String(length=40),
               type_=mysql.VARCHAR(length=100),
               existing_comment='邮箱',
               existing_nullable=False)
    op.alter_column('role', 'desc',
               existing_type=sa.String(length=50),
               type_=mysql.VARCHAR(length=20),
               existing_comment='描述',
               existing_nullable=True)
    op.alter_column('permission', 'desc',
               existing_type=sa.String(length=50),
               type_=mysql.VARCHAR(length=20),
               existing_comment='描述',
               existing_nullable=True)
    # ### end Alembic commands ###
