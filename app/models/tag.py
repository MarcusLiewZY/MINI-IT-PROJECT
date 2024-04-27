import uuid
from sqlalchemy.dialects.postgresql import UUID

from app import db


class Tag(db.Model):
    __tablename__ = "Tag"

    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = db.Column(db.String(20), nullable=False)
    color = db.Column(db.String(7), nullable=False)
    description = db.Column(db.String, nullable=False)
    created_at = db.Column(db.DateTime, nullable=False)
    updated_at = db.Column(db.DateTime, nullable=False)

    def __init__(self, tag_dist, *args, **kwargs):
        self.name = tag_dist.get("name")
        self.color = tag_dist.get("color")
        self.description = tag_dist.get("description")
        self.created_at = tag_dist.get("created_at")
        self.updated_at = self.created_at

    def __repr__(self):
        return f"<{self.name}>"
