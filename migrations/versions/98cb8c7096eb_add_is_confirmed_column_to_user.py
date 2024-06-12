"""add is_confirmed column to User

Revision ID: 98cb8c7096eb
Revises: 195cfb04d4e2
Create Date: 2024-06-12 11:07:14.554962

"""

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "98cb8c7096eb"
down_revision = "195cfb04d4e2"
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table("Comment", schema=None) as batch_op:
        batch_op.create_unique_constraint(None, ["id"])

    with op.batch_alter_table("CommentNotification", schema=None) as batch_op:
        batch_op.create_unique_constraint(None, ["id"])

    with op.batch_alter_table("Post", schema=None) as batch_op:
        batch_op.create_unique_constraint(None, ["id"])

    with op.batch_alter_table("PostNotification", schema=None) as batch_op:
        batch_op.create_unique_constraint(None, ["id"])

    with op.batch_alter_table("Tag", schema=None) as batch_op:
        batch_op.create_unique_constraint(None, ["id"])

    with op.batch_alter_table("User", schema=None) as batch_op:
        batch_op.add_column(
            sa.Column(
                "is_confirmed", sa.Boolean(), server_default="False", nullable=False
            )
        )
        batch_op.create_unique_constraint(None, ["id"])

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table("User", schema=None) as batch_op:
        batch_op.drop_constraint(None, type_="unique")
        batch_op.drop_column("is_confirmed")

    with op.batch_alter_table("Tag", schema=None) as batch_op:
        batch_op.drop_constraint(None, type_="unique")

    with op.batch_alter_table("PostNotification", schema=None) as batch_op:
        batch_op.drop_constraint(None, type_="unique")

    with op.batch_alter_table("Post", schema=None) as batch_op:
        batch_op.drop_constraint(None, type_="unique")

    with op.batch_alter_table("CommentNotification", schema=None) as batch_op:
        batch_op.drop_constraint(None, type_="unique")

    with op.batch_alter_table("Comment", schema=None) as batch_op:
        batch_op.drop_constraint(None, type_="unique")

    # ### end Alembic commands ###
