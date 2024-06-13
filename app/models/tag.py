from uuid import uuid4
from sqlalchemy.dialects.postgresql import UUID

from app import db


class Tag(db.Model):
    __tablename__ = "Tag"

    id = db.Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid4,
        unique=True,
        nullable=False,
        server_default=db.text("(gen_random_uuid())"),
    )
    name = db.Column(db.String(20), unique=True, nullable=False)
    color = db.Column(db.String(7), nullable=False)
    description = db.Column(db.Text, nullable=False)
    created_at = db.Column(
        db.DateTime(timezone=True), nullable=False, server_default=db.func.now()
    )
    updated_at = db.Column(
        db.DateTime(timezone=True), nullable=False, server_default=db.func.now()
    )

    def __init__(self, tag_dist, *args, **kwargs):
        self.name = tag_dist.get("name")
        self.color = tag_dist.get("color")
        self.description = tag_dist.get("description")
        self.created_at = tag_dist.get("created_at")
        self.updated_at = self.created_at

    def __repr__(self):
        return f"<{self.name}>"
