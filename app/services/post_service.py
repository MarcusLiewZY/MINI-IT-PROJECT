from datetime import datetime
from typing import List, Dict, Union, Tuple
from flask_login import current_user

from app.models import Post, Status, User, Tag
from app.dto.post_dto import PostDTO
from app import db, app
from app.forms import CreatePostForm
from app.utils.helper import format_datetime, upload_image, delete_image


def create_post(form: CreatePostForm) -> Tuple[bool, str]:
    """
    Create a post.
    Args:
        form (CreatePostForm): The form containing the post data.
    Returns:
        Tuple[bool, str]: A tuple containing a boolean indicating if the post was created successfully and a message.
    """
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
        return (False,)


def get_posts(
    user: User, isPreview: bool = False, page: int = 1, per_page: int = 10
) -> Tuple[bool, List[Dict[str, Union[str, int, bool, List]]]]:
    """
    Get all posts ordered by updated_at in descending order by default.
    Args:
        user (User): The user who is currently logged in.
        isPreview (bool): A flag to determine if the post is a preview.
    Returns:
        Tuple[List[Dict[str, Union[str, int, bool, List]]]]: A tuple containing a boolean indicating if there are more posts and a list of post DTOs.
    """
    posts = (
        Post.query.filter(Post.status == Status.APPROVED, Post.is_delete == False)
        .order_by(Post.updated_at.desc())
        .paginate(page=page, per_page=per_page, error_out=False)
    )

    has_next = posts.has_next
    post_list = posts.items

    postDTOs = [
        PostDTO(post, post.postCreator, user, isPreview).to_dict() for post in post_list
    ]

    return has_next, postDTOs


def edit_post(post: Post, form: CreatePostForm) -> Tuple[bool, str]:
    """
    Edit a post.
    Args:
        post (Post): The post instance to edit.
        form (CreatePostForm): The submitted form data to edit the post.
    Returns:
        Tuple[bool, str]: A tuple containing a boolean indicating if the post was edited successfully and a flash message.
    """
    try:
        cloudinary_image_url = None
        if form.image_url.data:
            old_image_url = post.image_url

            if old_image_url:
                isDeleted = delete_image(old_image_url)

                if not isDeleted:
                    return False, "Failed to edit post, please try again"

            cloudinary_image_url = upload_image(
                form.image_url.data, app.config["CLOUDINARY_POST_IMAGE_FOLDER"]
            )

            if cloudinary_image_url is None:
                return False, "Image upload failed, please try again"

        post.title = form.title.data
        post.content = form.content.data
        post.image_url = cloudinary_image_url
        post.updated_at = format_datetime(datetime.now())

        post.tags.clear()  # remove all tags

        for tag_name in form.tags.data:
            post.tags.append(Tag.query.filter(Tag.name == tag_name).first())

        # todo: set the status to pending once the admin feature is implemented

        db.session.commit()

        return True, "Post edited successfully"

    except Exception as e:
        print(e)
        return False, "Failed to edit post, please try again"
