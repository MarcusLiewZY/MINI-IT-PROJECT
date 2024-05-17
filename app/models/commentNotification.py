import uuid
from sqlalchemy.dialects.postgresql import UUID

from app import db


class CommentNotification(db.Model):
    __tablename__ = "CommentNotification"

    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    is_read = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.Text, nullable=False)
    user_id = db.Column(UUID(as_uuid=True), db.ForeignKey("User.id"))
    comment_id = db.Column(UUID(as_uuid=True), db.ForeignKey("Comment.id"))
    unread_comment_id = db.Column(UUID(as_uuid=True), db.ForeignKey("Comment.id"))

    # relationship

    def __init__(self, comment_notification_dict, *args, **kwargs):
        self.is_read = comment_notification_dict.get("is_read", False)
        self.user_id = comment_notification_dict.get("user_id")
        self.comment_id = comment_notification_dict.get("comment_id")
        self.unread_comment_id = comment_notification_dict.get("unread_comment_id")
        self.created_at = comment_notification_dict.get("created_at")

    def __repr__(self):
        return f"<CommentNotification-{self.id} - {self.is_read}>"
