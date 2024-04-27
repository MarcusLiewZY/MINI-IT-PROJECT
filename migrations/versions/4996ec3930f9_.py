"""empty message

Revision ID: 4996ec3930f9
Revises: ca44332a78cf
Create Date: 2024-04-27 09:17:59.435935

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '4996ec3930f9'
down_revision = 'ca44332a78cf'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('user', schema=None) as batch_op:
        batch_op.alter_column('id',
               existing_type=sa.NUMERIC(),
               type_=sa.UUID(),
               existing_nullable=False)

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('user', schema=None) as batch_op:
        batch_op.alter_column('id',
               existing_type=sa.UUID(),
               type_=sa.NUMERIC(),
               existing_nullable=False)

    # ### end Alembic commands ###
