import uuid, random
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
    db.Column("user_id", UUID(as_uuid=True), db.ForeignKey("User.id")),
    db.Column("post_id", UUID(as_uuid=True), db.ForeignKey("Post.id")),
)

PostBookmark = db.Table(
    "PostBookmark",
    db.Column("user_id", UUID(as_uuid=True), db.ForeignKey("User.id")),
    db.Column("post_id", UUID(as_uuid=True), db.ForeignKey("Post.id")),
)

CommentLike = db.Table(
    "CommentLike",
    db.Column("user_id", UUID(as_uuid=True), db.ForeignKey("User.id")),
    db.Column("comment_id ", UUID(as_uuid=True), db.ForeignKey("Comment.id")),
)


class User(UserMixin, db.Model):
    __tablename__ = "User"

    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    email = db.Column(db.String(60), unique=True, nullable=False)
    anon_no = db.Column(db.String(4), nullable=True)
    password = db.Column(db.String(60), nullable=False)
    username = db.Column(db.String(60), nullable=False)
    avatar_url = db.Column(db.String(200))
    campus = db.Column(db.Enum(Campus), default=Campus.NONE)
    is_admin = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.Text, nullable=False)
    updated_at = db.Column(db.Text, nullable=False)

    # relationship
    posts = db.relationship(
        "Post", backref="post", cascade="all, delete-orphan", lazy=True
    )
    liked_posts = db.relationship(
        "Post", secondary=PostLike, backref="liked_by", lazy=True
    )
    bookmarked_posts = db.relationship(
        "Post", secondary=PostBookmark, backref="bookmarked_by", lazy=True
    )
    comments = db.relationship(
        "Comment", backref="post", cascade="all, delete-orphan", lazy=True
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
        self.anon_no = self.generate_anon_no()
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
