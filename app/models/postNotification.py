from uuid import uuid4
from sqlalchemy.dialects.postgresql import UUID

from app import db


class PostNotification(db.Model):
    __tablename__ = "PostNotification"

    id = db.Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid4,
        unique=True,
        nullable=False,
        server_default=db.text("(gen_random_uuid())"),
    )
    is_read = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, nullable=False, server_default=db.func.now())

    # Foreign keys
    user_id = db.Column(UUID(as_uuid=True), db.ForeignKey("User.id"))
    post_id = db.Column(UUID(as_uuid=True), db.ForeignKey("Post.id"))
    unread_comment_id = db.Column(UUID(as_uuid=True), db.ForeignKey("Comment.id"))

    def __init__(self, post_notification_dict, *args, **kwargs):
        self.is_read = post_notification_dict.get("is_read", False)
        self.user_id = post_notification_dict.get("user_id")
        self.post_id = post_notification_dict.get("post_id")
        self.unread_comment_id = post_notification_dict.get("unread_comment_id")
        self.created_at = post_notification_dict.get("created_at")
        self.updated_at = self.created_at

    def __repr__(self):
        return f"<PostNotifications-{self.id} - {self.is_read}>"
