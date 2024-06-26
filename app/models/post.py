from uuid import uuid4
from sqlalchemy.dialects.postgresql import UUID
from enum import Enum

from app import db


class PostStatus(Enum):
    PENDING = "Pending"
    APPROVED = "Approved"
    REJECTED = "Rejected"
    UNREAD_APPROVED = "Unread_approved"
    UNREAD_REJECTED = "Unread_rejected"


PostTag = db.Table(
    "PostTag",
    db.Column(
        "post_id", UUID(as_uuid=True), db.ForeignKey("Post.id", ondelete="CASCADE")
    ),
    db.Column(
        "tag_id", UUID(as_uuid=True), db.ForeignKey("Tag.id", ondelete="CASCADE")
    ),
)


class Post(db.Model):
    __tablename__ = "Post"

    id = db.Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid4,
        unique=True,
        nullable=False,
        server_default=db.text("(gen_random_uuid())"),
    )
    title = db.Column(db.String(120), nullable=False)
    content = db.Column(db.Text, nullable=False)
    image_url = db.Column(db.String(120))
    is_delete = db.Column(db.Boolean, default=False)
    status = db.Column(db.Enum(PostStatus), nullable=False)
    updated_at = db.Column(
        db.DateTime(timezone=True), nullable=False, server_default=db.func.now()
    )
    created_at = db.Column(
        db.DateTime(timezone=True), nullable=False, server_default=db.func.now()
    )

    # Foreign keys
    user_id = db.Column(
        UUID(as_uuid=True), db.ForeignKey("User.id", ondelete="CASCADE")
    )

    # relationship
    tags = db.relationship(
        "Tag",
        secondary=PostTag,
        backref="posts",
        lazy=True,
    )
    comments = db.relationship(
        "Comment", backref="commented_post", cascade="all, delete-orphan", lazy=True
    )

    post_notifications = db.relationship(
        "PostNotification",
        backref="notified_post_by_post",
        cascade="all, delete-orphan",
        lazy=True,
    )

    def __init__(self, post_dist, *args, **kwargs):
        self.title = post_dist.get("title")
        self.content = post_dist.get("content")
        self.image_url = post_dist.get("image_url")
        self.status = PostStatus.PENDING
        self.created_at = post_dist.get("created_at")
        self.updated_at = self.created_at

    def __repr__(self):
        return f"<{self.status} - {self.title[:40]}{'...' if len(self.title) >= 40 else ''}>"
