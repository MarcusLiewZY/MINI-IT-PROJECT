import uuid

from sqlalchemy.dialects.postgresql import UUID
from enum import Enum

from app import db


class Status(Enum):
    PENDING = "Pending"
    APPROVED = "Approved"
    REJECTED = "Rejected"


class Post(db.Model):
    __tablename__ = "post"

    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    title = db.Column(db.String(60), nullable=False)
    content = db.Column(db.String, nullable=False)
    image_url = db.Column(db.String(120))
    is_delete = db.Column(db.Boolean, default=False)
    status = db.Column(db.Enum(Status), nullable=False)
    created_at = db.Column(db.DateTime, nullable=False)
    updated_at = db.Column(db.DateTime, nullable=False)

    # relationship
    user_id = db.Column(UUID(as_uuid=True), db.ForeignKey("user.id"))

    def __init__(self, post_dist, *args, **kwargs):
        self.title = post_dist.get("title")
        self.content = post_dist.get("content")
        self.image_url = post_dist.get("image_url")
        self.status = Status.PENDING
        self.created_at = post_dist.get("created_at")
        self.updated_at = self.created_at

    def __repr__(self):
        return f"<{self.status} - {self.title[:40]}...>"
