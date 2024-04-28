import uuid
from sqlalchemy.dialects.postgresql import UUID

from app import db


class PostNotification(db.Model):
    __tablename__ = "PostNotification"

    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    is_read = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, nullable=False)
    user_id = db.Column(UUID(as_uuid=True), db.ForeignKey("User.id"))
    post_id = db.Column(UUID(as_uuid=True), db.ForeignKey("Post.id"))
    unread_comment_id = db.Column(UUID(as_uuid=True), db.ForeignKey("Comment.id"))

    # relationship

    def __init__(self, post_notification_dist, *args, **kwargs):
        self.created_at = post_notification_dist.get("created_at")

    def __repr__(self):
        return f"<{self.id} - {self.is_read}>"
