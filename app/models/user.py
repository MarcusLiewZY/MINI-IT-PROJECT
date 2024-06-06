from uuid import uuid4
import random
from flask_login import UserMixin
from sqlalchemy.dialects.postgresql import UUID
from enum import Enum

from app import db, bcrypt, login_manager


class Campus(Enum):
    CYBERJAYA = "Cyberjaya"
    MALACCA = "Malacca"
    NONE = "None"


PostLike = db.Table(
    "PostLike",
    db.Column(
        "user_id", UUID(as_uuid=True), db.ForeignKey("User.id", ondelete="CASCADE")
    ),
    db.Column(
        "post_id", UUID(as_uuid=True), db.ForeignKey("Post.id", ondelete="CASCADE")
    ),
    db.Column("created_at", db.Text, nullable=False),
)

PostBookmark = db.Table(
    "PostBookmark",
    db.Column(
        "user_id", UUID(as_uuid=True), db.ForeignKey("User.id", ondelete="CASCADE")
    ),
    db.Column(
        "post_id", UUID(as_uuid=True), db.ForeignKey("Post.id", ondelete="CASCADE")
    ),
    db.Column("created_at", db.Text, nullable=False),
)

CommentLike = db.Table(
    "CommentLike",
    db.Column(
        "user_id", UUID(as_uuid=True), db.ForeignKey("User.id", ondelete="CASCADE")
    ),
    db.Column(
        "comment_id",
        UUID(as_uuid=True),
        db.ForeignKey("Comment.id", ondelete="CASCADE"),
    ),
)


class User(UserMixin, db.Model):
    __tablename__ = "User"

    id = db.Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid4,
        unique=True,
        nullable=False,
        server_default=db.text("(gen_random_uuid())"),
    )
    email = db.Column(db.String(60), unique=True, nullable=False)
    anon_no = db.Column(db.String(4), nullable=True)
    password = db.Column(db.String(200), nullable=False)
    username = db.Column(db.String(60), nullable=False)
    avatar_url = db.Column(db.String(200), nullable=True)
    campus = db.Column(db.Enum(Campus), default=Campus.NONE)
    is_admin = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, nullable=False, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, nullable=False, server_default=db.func.now())

    # relationship
    posts = db.relationship(
        "Post", backref="postCreator", cascade="all, delete-orphan", lazy=True
    )
    liked_posts = db.relationship(
        "Post", secondary=PostLike, backref="liked_by", lazy=True
    )
    bookmarked_posts = db.relationship(
        "Post", secondary=PostBookmark, backref="bookmarked_by", lazy=True
    )
    comments = db.relationship(
        "Comment", backref="commentCreator", cascade="all, delete-orphan", lazy=True
    )
    liked_comments = db.relationship(
        "Comment", secondary=CommentLike, backref="liked_by", lazy=True
    )
    post_notifications = db.relationship(
        "PostNotification",
        backref="notified_user_by_post",
        cascade="all, delete-orphan",
        lazy=True,
    )
    comment_notifications = db.relationship(
        "CommentNotification",
        backref="notified_user_by_comment",
        cascade="all, delete-orphan",
        lazy=True,
    )

    def __init__(self, user_dict, *args, **kwargs):
        self.email = user_dict.get("email")
        self.anon_no = None  # only assign when the user accept the community guidelines
        self.password = bcrypt.generate_password_hash(user_dict.get("password"))
        self.username = user_dict.get("username")
        self.avatar_url = user_dict.get("avatar_url")
        self.campus = user_dict.get("campus")
        self.is_admin = user_dict.get("is_admin")
        self.created_at = user_dict.get("created_at")
        self.updated_at = self.created_at

    def __repr__(self):
        return f"<User {self.username} with email {self.email}>"

    # four random digits, exp: 3932
    @staticmethod
    def generate_anon_no():
        random_no = [random.randint(0, 9) for _ in range(4)]
        return "".join(map(str, random_no))


# The user_loader callback is used to reload the user object from the user ID stored in the session.
@login_manager.user_loader
def user_loader(user_id):
    # user_id = user_id
    if not user_id:
        return None  # Return None if user_id is not a valid UUID

    return User.query.filter(User.id == user_id).first()
