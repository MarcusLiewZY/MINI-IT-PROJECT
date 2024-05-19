from datetime import datetime
from typing import List, Dict, Union, Tuple
from flask_login import current_user

from app.models import Post, Status, PostLike, PostBookmark, User, Tag, Comment
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

        post.status = Status.PENDING
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
    Get posts ordered by updated_at in descending order by default based on the pagination parameters (page and per_page)
    Args:
        user (User): The user who is currently logged in.
        isPreview (bool): A flag to determine if the post is a preview.
        page (int): The page number of the post list.
        per_page (int): The number of the posts per page.
    Returns:
        Tuple[List[Dict[str, Union[str, int, bool, List]]]]: A tuple containing a boolean indicating if there are more posts and a list of post DTOs.
    """
    posts = (
        Post.query.filter(
            Post.status.in_([Status.APPROVED, Status.UNREAD_APPROVED]),
            Post.is_delete == False,
        )
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

        tags_to_remove = []
        for tag in post.tags:
            if tag.name not in form.tags.data:
                tags_to_remove.append(tag)

        tags_to_add = []
        for tag_name in form.tags.data:
            tag = Tag.query.filter(Tag.name == tag_name).first()
            if tag and tag not in post.tags:
                tags_to_add.append(tag)

        for tag in tags_to_remove:
            post.tags.remove(tag)

        for tag_name in tags_to_add:
            tag = Tag.query.filter(Tag.name == tag_name).first()
            if tag:
                post.tags.append(tag)

        post.status = Status.PENDING

        db.session.commit()

        return True, "Post edited successfully"

    except Exception as e:
        db.session.rollback()
        print(e)
        return False, "Failed to edit post, please try again"


def get_created_posts(
    user: User, isPreview: bool = False, page: int = 1, per_page: int = 10
) -> Tuple[bool, List[Dict[str, Union[str, int, bool, List]]]]:
    """
    Get posts created by the user ordered by updated_at in descending order by default based on the pagination parameters (page and per_page)
    Args:
        user (User): The user who is currently logged in.
        isPreview (bool): A flag to determine if the post is a preview.
        page (int): The page number of the post list.
        per_page (int): The number of the posts per page.
    Returns:
        Tuple[List[Dict[str, Union[str, int, bool, List]]]]: A tuple containing a boolean indicating if there are more posts and a list of post DTOs.
    """

    created_posts = (
        Post.query.filter(
            Post.user_id == user.id,
            Post.status.in_([Status.APPROVED, Status.UNREAD_APPROVED]),
            Post.is_delete == False,
        )
        .order_by(Post.updated_at.desc())
        .paginate(page=page, per_page=per_page, error_out=False)
    )

    has_next = created_posts.has_next
    post_list = created_posts.items

    postDTOs = [
        PostDTO(post, post.postCreator, user, isPreview).to_dict() for post in post_list
    ]

    return has_next, postDTOs


def get_liked_posts(
    user: User, isPreview: bool = False, page: int = 1, per_page: int = 10
) -> Tuple[bool, List[Dict[str, Union[str, int, bool, List]]]]:
    """
    Get posts liked by the user ordered by updated_at in descending order by default based on the pagination parameter (page and per_page)
    Args:
        user (User): The user who is currently logged in.
        isPreview (bool): A flag to determine if the post is a preview.
        page (int): The page number of the post list.
        per_page (int): The number of the posts per page.
    Returns:
        Tuple[List[Dict[str, Union[str, int, bool, List]]]]: A tuple containing a boolean indicating if there are more posts and a list of post DTOs.
    """

    liked_posts = (
        Post.query.filter(
            Post.status_in_([Status.APPROVED, Status.UNREAD_APPROVED]),
            Post.is_delete == False,
        )
        .join(PostLike, PostLike.c.post_id == Post.id)
        .filter(PostLike.c.user_id == user.id)
        .order_by(PostLike.c.created_at.desc())
        .paginate(page=page, per_page=per_page, error_out=False)
    )

    has_next = liked_posts.has_next
    post_list = liked_posts.items

    postDTOs = [
        PostDTO(post, post.postCreator, user, isPreview=isPreview).to_dict()
        for post in post_list
    ]

    return has_next, postDTOs


def get_replies_posts(
    user: User, isPreview: bool = False, page: int = 1, per_page: int = 10
) -> Tuple[bool, List[Dict[str, Union[str, int, bool, List]]]]:
    """
    Get posts replied by the user ordered by updated_at in descending order by default based on the pagination parameter (page and per_page)
    Args:
        user (User): The user who is currently logged in.
        isPreview (bool): A flag to determine if the post is a preview.
        page (int): The page number of the post list.
        per_page (int): The number of the posts per page.
    Returns:
        Tuple[List[Dict[str, Union[str, int, bool, List]]]]: A tuple containing a boolean indicating if there are more posts and a list of post DTOs.
    """

    comments = (
        Comment.query.filter(Comment.user_id == user.id)
        .order_by(Comment.updated_at.desc())
        .all()
    )

    # We need to get the unique ordered posts that the user has commented on.
    # We cannot use set only because the order of the posts will be lost.
    # Thus, we will use a set to keep track of the posts that we have seen, and a list to keep the order of the posts.
    all_commented_posts = []
    seen_posts = set()

    for comment in comments:
        commented_post = comment.commented_post
        if (
            commented_post.status in [Status.APPROVED, Status.UNREAD_APPROVED]
            and not commented_post.is_delete
        ):
            if commented_post not in seen_posts:
                all_commented_posts.append(commented_post)
                seen_posts.add(commented_post)

    start = (page - 1) * per_page
    end = start + per_page

    post_list = list(all_commented_posts)[start:end]
    has_next = end < len(all_commented_posts)

    postDTOs = [
        PostDTO(
            commented_post,
            commented_post.postCreator,
            user,
            isPreview=isPreview,
        )
        for commented_post in post_list
    ]

    return has_next, postDTOs


def get_bookmarked_posts(
    user: User, isPreview: bool = False, page: int = 1, per_page: int = 10
) -> Tuple[bool, List[Dict[str, Union[str, int, bool, List]]]]:
    """
    Get posts bookmarked by the user ordered by updated_at in descending order by default based on the pagination parameter (page and per_page)
    Args:
        user (User): The user who is currently logged in.
        isPreview (bool): A flag to determine if the post is a preview.
        page (int): The page number of the post list.
        per_page (int): The number of the posts per page.
    Returns:
        Tuple[List[Dict[str, Union[str, int, bool, List]]]]: A tuple containing a boolean indicating if there are more posts and a list of post DTOs.
    """

    bookmarked_posts = (
        Post.query.filter(
            Post.status.in_([Status.APPROVED, Status.UNREAD_APPROVED]),
            Post.is_delete == False,
        )
        .join(PostBookmark, PostBookmark.c.post_id == Post.id)
        .filter(PostBookmark.c.user_id == user.id)
        .order_by(PostBookmark.c.created_at.desc())
        .paginate(page=page, per_page=per_page, error_out=False)
    )

    has_next = bookmarked_posts.has_next
    post_list = bookmarked_posts.items

    postDTOs = [
        PostDTO(post, post.postCreator, user, isPreview=isPreview).to_dict()
        for post in post_list
    ]

    return has_next, postDTOs
