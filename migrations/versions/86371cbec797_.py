"""empty message

Revision ID: 86371cbec797
Revises: b28f723e64d4
Create Date: 2020-02-23 16:50:06.188072

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '86371cbec797'
down_revision = 'b28f723e64d4'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('address',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('phone', sa.String(length=11), nullable=False),
    sa.Column('username', sa.String(length=50), nullable=False),
    sa.Column('address', sa.Text(), nullable=False),
    sa.Column('create_time', sa.DateTime(), nullable=True),
    sa.Column('is_address', sa.String(length=2), nullable=False),
    sa.Column('status', sa.String(length=2), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.add_column('user', sa.Column('address', sa.String(length=256), nullable=False))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('user', 'address')
    op.drop_table('address')
    # ### end Alembic commands ###
