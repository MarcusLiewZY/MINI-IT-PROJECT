import uuid, random
from flask_login import UserMixin
from sqlalchemy.dialects.postgresql import UUID
from enum import Enum

from app import db, bcrypt, login_manager


class Campus(Enum):
    CYBERJAYA = "Cyberjaya"
    MALACCA = "Malacca"
    NONE = "None"


class User(UserMixin, db.Model):
    __tablename__ = "user"

    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    email = db.Column(db.String(60), unique=True, nullable=False)
    anon_no = db.Column(db.String(4), nullable=True)
    password = db.Column(db.String(60), nullable=False)
    username = db.Column(db.String(60), nullable=False)
    avatar_url = db.Column(db.String(200))
    campus = db.Column(db.Enum(Campus), default=Campus.NONE)
    is_admin = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, nullable=False)
    updated_at = db.Column(db.DateTime, nullable=False)

    # relationship
    posts = db.relationship(
        "Post", backref="post", cascade="all, delete-orphan", lazy=True
    )

    def __init__(self, user_dist, *args, **kwargs):
        self.email = user_dist.get("email")
        self.anon_no = self.generate_anon_no()
        self.password = bcrypt.generate_password_hash(user_dist.get("password"))
        self.username = user_dist.get("username")
        self.avatar_url = user_dist.get("avatar_url")
        self.campus = user_dist.get("campus")
        self.is_admin = user_dist.get("is_admin")
        self.created_at = user_dist.get("created_at")
        self.updated_at = self.created_at

    def __repr__(self):
        return f"<User {self.username} with email {self.email}>"

    # four random digits, exp: 3932
    def generate_anon_no(self):
        random_no = [random.randint(0, 9) for _ in range(4)]
        return "".join(map(str, random_no))


@login_manager.user_loader
def user_loader(user_id):
    try:
        user_id = uuid.UUID(user_id)
    except ValueError:
        return None  # Return None if user_id is not a valid UUID

    return User.query.filter(User.id == user_id).first()
