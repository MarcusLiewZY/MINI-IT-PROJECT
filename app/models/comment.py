from uuid import uuid4
from sqlalchemy.dialects.postgresql import UUID
from enum import Enum

from app import db


class CommentStatus(Enum):
    NOT_REPORTED = "Not_reported"
    REPORTED = "Reported"
    ALLOWED = "Allowed"


class Comment(db.Model):
    __tablename__ = "Comment"

    id = db.Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid4,
        unique=True,
        nullable=False,
        server_default=db.text("(gen_random_uuid())"),
    )
    content = db.Column(db.Text, nullable=False)
    status = db.Column(
        db.Enum(CommentStatus),
        nullable=False,
    )
    created_at = db.Column(db.DateTime, nullable=False, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, nullable=False, server_default=db.func.now())

    # Foreign keys
    user_id = db.Column(UUID(as_uuid=True), db.ForeignKey("User.id"))
    post_id = db.Column(UUID(as_uuid=True), db.ForeignKey("Post.id"))
    replied_comment_id = db.Column(UUID(as_uuid=True), db.ForeignKey("Comment.id"))

    # relationship
    # self-referential relationship
    # from child to parent
    # reply_comment = child.replied_comment or child.replied_comment_id
    # from parent to child using backref
    # replied_comment = parent.replies
    replied_comment = db.relationship(
        "Comment", remote_side=[id], backref="replies", lazy=True, uselist=False
    )
    notify_post = db.relationship(
        "PostNotification",
        backref="unread_comment_to_post",
        cascade="all, delete-orphan",
        uselist=False,
        lazy=True,
    )
    comment_notifications = db.relationship(
        "CommentNotification",
        backref="notified_comment_by_comment",
        cascade="all, delete-orphan",
        lazy=True,
        foreign_keys="[CommentNotification.comment_id]",
    )
    notify_comment = db.relationship(
        "CommentNotification",
        backref="unread_comment_to_comment",
        cascade="all, delete-orphan",
        uselist=False,
        lazy=True,
        foreign_keys="[CommentNotification.unread_comment_id]",
    )

    def __init__(self, comment_dist, *args, **kwargs):
        self.content = comment_dist.get("content")
        self.status = CommentStatus.NOT_REPORTED
        self.created_at = comment_dist.get("created_at")
        self.updated_at = self.created_at

    def __repr__(self):
        return f'<{self.content[:40]}{"..." if len(self.content) >= 40 else ""}>'
