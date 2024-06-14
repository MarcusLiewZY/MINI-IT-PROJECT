from uuid import uuid4
from sqlalchemy.dialects.postgresql import UUID

from app import db


class CommentNotification(db.Model):
    __tablename__ = "CommentNotification"

    id = db.Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid4,
        unique=True,
        nullable=False,
        server_default=db.text("(gen_random_uuid())"),
    )
    is_read = db.Column(db.Boolean, default=False)
    created_at = db.Column(
        db.DateTime(timezone=True), nullable=False, server_default=db.func.now()
    )

    # Foreign keys
    user_id = db.Column(
        UUID(as_uuid=True), db.ForeignKey("User.id", ondelete="CASCADE")
    )
    comment_id = db.Column(
        UUID(as_uuid=True), db.ForeignKey("Comment.id", ondelete="CASCADE")
    )
    unread_comment_id = db.Column(
        UUID(as_uuid=True), db.ForeignKey("Comment.id", ondelete="CASCADE")
    )

    # relationship

    def __init__(self, comment_notification_dict, *args, **kwargs):
        self.is_read = comment_notification_dict.get("is_read", False)
        self.user_id = comment_notification_dict.get("user_id")
        self.comment_id = comment_notification_dict.get("comment_id")
        self.unread_comment_id = comment_notification_dict.get("unread_comment_id")
        self.created_at = comment_notification_dict.get("created_at")
        self.updated_at = self.created_at

    def __repr__(self):
        return f"<CommentNotification-{self.id} - {self.is_read}>"
