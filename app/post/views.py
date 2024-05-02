from flask import flash
from datetime import datetime

from . import post

from app import db
from app.models.post import Post, Status
from app.models.tag import Tag
from app.models.user import User
from app.utils.helper import format_datetime

# post
# post - tags
# user_id


def create_post(post, user):
    new_post = Post(
        {
            "title": post.get("title"),
            "content": post.get("content"),
            "image_url": post.get("image_url"),
            "created_at": format_datetime(datetime.now()),
        }
    )

    new_post.user_id = user.id

    # todo: delete the approved status once the admin feature is implemented
    new_post.status = Status.APPROVED

    for tag_name in post.get("tags", []):
        tag = Tag.query.filter_by(name=tag_name).first()
        if not tag:
            flash("Tag not found", "error")
            return False

        new_post.tags.append(tag)

    db.session.add(new_post)
    db.session.commit()

    return True
