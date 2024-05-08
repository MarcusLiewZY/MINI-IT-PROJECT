"""empty message

Revision ID: b9c98406f9b9
Revises: b32f97d14c2c
Create Date: 2024-05-06 10:06:15.068352

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'b9c98406f9b9'
down_revision = 'b32f97d14c2c'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('Comment', schema=None) as batch_op:
        batch_op.alter_column('id',
               existing_type=sa.NUMERIC(),
               type_=sa.UUID(),
               existing_nullable=False)
        batch_op.alter_column('user_id',
               existing_type=sa.NUMERIC(),
               type_=sa.UUID(),
               existing_nullable=True)
        batch_op.alter_column('post_id',
               existing_type=sa.NUMERIC(),
               type_=sa.UUID(),
               existing_nullable=True)
        batch_op.alter_column('replied_comment_id',
               existing_type=sa.NUMERIC(),
               type_=sa.UUID(),
               existing_nullable=True)

    with op.batch_alter_table('CommentLike', schema=None) as batch_op:
        batch_op.alter_column('user_id',
               existing_type=sa.NUMERIC(),
               type_=sa.UUID(),
               existing_nullable=True)
        batch_op.alter_column('comment_id ',
               existing_type=sa.NUMERIC(),
               type_=sa.UUID(),
               existing_nullable=True)

    with op.batch_alter_table('CommentNotification', schema=None) as batch_op:
        batch_op.alter_column('id',
               existing_type=sa.NUMERIC(),
               type_=sa.UUID(),
               existing_nullable=False)
        batch_op.alter_column('user_id',
               existing_type=sa.NUMERIC(),
               type_=sa.UUID(),
               existing_nullable=True)
        batch_op.alter_column('comment_id',
               existing_type=sa.NUMERIC(),
               type_=sa.UUID(),
               existing_nullable=True)
        batch_op.alter_column('unread_comment_id',
               existing_type=sa.NUMERIC(),
               type_=sa.UUID(),
               existing_nullable=True)

    with op.batch_alter_table('Post', schema=None) as batch_op:
        batch_op.alter_column('id',
               existing_type=sa.NUMERIC(),
               type_=sa.UUID(),
               existing_nullable=False)
        batch_op.alter_column('user_id',
               existing_type=sa.NUMERIC(),
               type_=sa.UUID(),
               existing_nullable=True)

    with op.batch_alter_table('PostBookmark', schema=None) as batch_op:
        batch_op.alter_column('user_id',
               existing_type=sa.NUMERIC(),
               type_=sa.UUID(),
               existing_nullable=True)
        batch_op.alter_column('post_id',
               existing_type=sa.NUMERIC(),
               type_=sa.UUID(),
               existing_nullable=True)

    with op.batch_alter_table('PostLike', schema=None) as batch_op:
        batch_op.alter_column('user_id',
               existing_type=sa.NUMERIC(),
               type_=sa.UUID(),
               existing_nullable=True)
        batch_op.alter_column('post_id',
               existing_type=sa.NUMERIC(),
               type_=sa.UUID(),
               existing_nullable=True)

    with op.batch_alter_table('PostNotification', schema=None) as batch_op:
        batch_op.alter_column('id',
               existing_type=sa.NUMERIC(),
               type_=sa.UUID(),
               existing_nullable=False)
        batch_op.alter_column('user_id',
               existing_type=sa.NUMERIC(),
               type_=sa.UUID(),
               existing_nullable=True)
        batch_op.alter_column('post_id',
               existing_type=sa.NUMERIC(),
               type_=sa.UUID(),
               existing_nullable=True)
        batch_op.alter_column('unread_comment_id',
               existing_type=sa.NUMERIC(),
               type_=sa.UUID(),
               existing_nullable=True)

    with op.batch_alter_table('PostTag', schema=None) as batch_op:
        batch_op.alter_column('post_id',
               existing_type=sa.NUMERIC(),
               type_=sa.UUID(),
               existing_nullable=True)
        batch_op.alter_column('tag_id',
               existing_type=sa.NUMERIC(),
               type_=sa.UUID(),
               existing_nullable=True)

    with op.batch_alter_table('Tag', schema=None) as batch_op:
        batch_op.alter_column('id',
               existing_type=sa.NUMERIC(),
               type_=sa.UUID(),
               existing_nullable=False)

    with op.batch_alter_table('User', schema=None) as batch_op:
        batch_op.alter_column('id',
               existing_type=sa.NUMERIC(),
               type_=sa.UUID(),
               existing_nullable=False)

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('User', schema=None) as batch_op:
        batch_op.alter_column('id',
               existing_type=sa.UUID(),
               type_=sa.NUMERIC(),
               existing_nullable=False)

    with op.batch_alter_table('Tag', schema=None) as batch_op:
        batch_op.alter_column('id',
               existing_type=sa.UUID(),
               type_=sa.NUMERIC(),
               existing_nullable=False)

    with op.batch_alter_table('PostTag', schema=None) as batch_op:
        batch_op.alter_column('tag_id',
               existing_type=sa.UUID(),
               type_=sa.NUMERIC(),
               existing_nullable=True)
        batch_op.alter_column('post_id',
               existing_type=sa.UUID(),
               type_=sa.NUMERIC(),
               existing_nullable=True)

    with op.batch_alter_table('PostNotification', schema=None) as batch_op:
        batch_op.alter_column('unread_comment_id',
               existing_type=sa.UUID(),
               type_=sa.NUMERIC(),
               existing_nullable=True)
        batch_op.alter_column('post_id',
               existing_type=sa.UUID(),
               type_=sa.NUMERIC(),
               existing_nullable=True)
        batch_op.alter_column('user_id',
               existing_type=sa.UUID(),
               type_=sa.NUMERIC(),
               existing_nullable=True)
        batch_op.alter_column('id',
               existing_type=sa.UUID(),
               type_=sa.NUMERIC(),
               existing_nullable=False)

    with op.batch_alter_table('PostLike', schema=None) as batch_op:
        batch_op.alter_column('post_id',
               existing_type=sa.UUID(),
               type_=sa.NUMERIC(),
               existing_nullable=True)
        batch_op.alter_column('user_id',
               existing_type=sa.UUID(),
               type_=sa.NUMERIC(),
               existing_nullable=True)

    with op.batch_alter_table('PostBookmark', schema=None) as batch_op:
        batch_op.alter_column('post_id',
               existing_type=sa.UUID(),
               type_=sa.NUMERIC(),
               existing_nullable=True)
        batch_op.alter_column('user_id',
               existing_type=sa.UUID(),
               type_=sa.NUMERIC(),
               existing_nullable=True)

    with op.batch_alter_table('Post', schema=None) as batch_op:
        batch_op.alter_column('user_id',
               existing_type=sa.UUID(),
               type_=sa.NUMERIC(),
               existing_nullable=True)
        batch_op.alter_column('id',
               existing_type=sa.UUID(),
               type_=sa.NUMERIC(),
               existing_nullable=False)

    with op.batch_alter_table('CommentNotification', schema=None) as batch_op:
        batch_op.alter_column('unread_comment_id',
               existing_type=sa.UUID(),
               type_=sa.NUMERIC(),
               existing_nullable=True)
        batch_op.alter_column('comment_id',
               existing_type=sa.UUID(),
               type_=sa.NUMERIC(),
               existing_nullable=True)
        batch_op.alter_column('user_id',
               existing_type=sa.UUID(),
               type_=sa.NUMERIC(),
               existing_nullable=True)
        batch_op.alter_column('id',
               existing_type=sa.UUID(),
               type_=sa.NUMERIC(),
               existing_nullable=False)

    with op.batch_alter_table('CommentLike', schema=None) as batch_op:
        batch_op.alter_column('comment_id ',
               existing_type=sa.UUID(),
               type_=sa.NUMERIC(),
               existing_nullable=True)
        batch_op.alter_column('user_id',
               existing_type=sa.UUID(),
               type_=sa.NUMERIC(),
               existing_nullable=True)

    with op.batch_alter_table('Comment', schema=None) as batch_op:
        batch_op.alter_column('replied_comment_id',
               existing_type=sa.UUID(),
               type_=sa.NUMERIC(),
               existing_nullable=True)
        batch_op.alter_column('post_id',
               existing_type=sa.UUID(),
               type_=sa.NUMERIC(),
               existing_nullable=True)
        batch_op.alter_column('user_id',
               existing_type=sa.UUID(),
               type_=sa.NUMERIC(),
               existing_nullable=True)
        batch_op.alter_column('id',
               existing_type=sa.UUID(),
               type_=sa.NUMERIC(),
               existing_nullable=False)

    # ### end Alembic commands ###
