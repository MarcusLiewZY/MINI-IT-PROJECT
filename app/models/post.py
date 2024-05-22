import uuid
from sqlalchemy.dialects.postgresql import UUID
from enum import Enum

from app import db


            
class Status(Enum):
    PENDING = "Pending"
    APPROVED = "Approved"
    REJECTED = "Rejected"
    UNREAD_APPROVED = "Unread_approved"
    UNREAD_REJECTED = "Unread_rejected"


PostTag = db.Table(
    "PostTag",
    db.Column("post_id", UUID(as_uuid=True), db.ForeignKey("Post.id")),
    db.Column("tag_id", UUID(as_uuid=True), db.ForeignKey("Tag.id")),
)


class Post(db.Model):
    __tablename__ = "Post"
    
    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    title = db.Column(db.String(120), nullable=False)
    content = db.Column(db.Text, nullable=False)
    image_url = db.Column(db.String(120))
    is_delete = db.Column(db.Boolean, default=False)
    status = db.Column(db.Enum(Status), nullable=False)
    updated_at = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.Text, nullable=False)

    user_id = db.Column(UUID(as_uuid=True), db.ForeignKey("User.id"))

    # relationship
    tags = db.relationship(
        "Tag",   
        secondary=PostTag,
        backref="posts",
        lazy=True,
    )
    comments = db.relationship(
        "Comment",
        backref = "commented_post",
        cascade= "all, delete-orphan",
        lazy = True
    )
    
    post_notifications = db.relationship(
        "PostNotification",
        backref = "notified_post_by_post",
        cascade = "all, delete-orphan",
        lazy = True
    )

    def __init__(self, post_dist, *args, **kwargs):
        self.title = post_dist.get("title") 
        self.content = post_dist.get("content")
        self.image_url = post_dist.get("image_url")
        self.status = Status.PENDING
        self.created_at = post_dist.get("created_at")
        self.updated_at = self.created_at

    def __repr__(self):
        return f"<{self.status} - {self.title[:40]}{"..." if len(self.title) >= 40 else ""}>"

