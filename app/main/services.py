from datetime import datetime
from flask import flash
from flask_login import current_user
from typing import Tuple

from app import db, app
from app.post.forms import CreatePostForm
from app.models.post import Post, Status
from app.models.tag import Tag
from app.utils.helper import format_datetime, upload_image


def create_post(form: CreatePostForm) -> Tuple[bool, str]:
    try:
        cloudinary_image_url = None
        if form.image_url.data:
            cloudinary_image_url = upload_image(
                form.image_url.data,
                app.config["CLOUDINARY_POST_IMAGE_FOLDER"],
            )
            if cloudinary_image_url is None:
                return False, "Image upload failed, please try again"

        post = Post(
            {
                "title": form.title.data,
                "content": form.content.data,
                "image_url": cloudinary_image_url,
                "created_at": format_datetime(datetime.now()),
            }
        )

        db.session.add(post)

        for tag_name in form.tags.data:
            post.tags.append(Tag.query.filter_by(name=tag_name).first())

        # todo: set the status to pending once the admin feature is implemented
        post.status = Status.APPROVED
        post.user_id = current_user.id
        db.session.commit()
        return True, "Post created successfully"

    except Exception as e:
        print(e)
        return False, "Post creation failed, please try again"
