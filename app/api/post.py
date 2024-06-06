from werkzeug.datastructures import MultiDict
import json
from datetime import datetime
from uuid import UUID
from sqlalchemy import select, insert, delete
from flask import jsonify, request
from flask_login import current_user
from http import HTTPStatus as responseStatus

from . import api
from app import db
from app.models import PostLike, PostBookmark, Post, PostStatus
from app.services.post_service import create_post as create_post_service
from app.forms import CreatePostForm
from app.dto.post_dto import PostDTO
from app.utils.api_utils import error_message
from app.utils.decorators import api_login_required, api_is_admin

#Retrieves all posts based on optional query parameters (isPreview, isDeleted, isApproved)
@api.route("/posts", methods=["GET"])
@api_login_required
def get_posts():
    """
    Get all posts ordered by the updated_at field in descending order.
    Args:
        isPreview: A boolean indicating whether to return a preview of the post. Default is False.
        isDeleted: A boolean indicating whether to return the soft deleted posts. Default is False.
        isApproved: A boolean indicating whether to return approved posts. Default is False.
    Returns:
        A JSON object containing all posts and an HTTP status code.
    """
    try:
        isPreview = request.args.get("isPreview", "false").lower() == "true"
        isDeleted = request.args.get("isDeleted", "false").lower() == "true"
        isApproved = request.args.get("isApproved", "true").lower() == "true"

        query = Post.query

        if isDeleted:
            query = query.filter(Post.is_delete == True)

        if isApproved:
            query = query.filter(
                Post.status.in_([PostStatus.APPROVED, PostStatus.UNREAD_APPROVED])
            )

        posts = query.order_by(Post.updated_at.desc()).all()
        postDTOs = [
            PostDTO(post, post.postCreator, post.postCreator, isPreview).to_dict()
            for post in posts2
        ]

        return (
            jsonify({"status": responseStatus.OK, "posts": postDTOs}),
            responseStatus.OK,
        )

    except Exception as e:
        print(e)
        return error_message(
            "Internal Server Error", responseStatus.INTERNAL_SERVER_ERROR
        )


@api.route("/posts", methods=["POST"])
@api_login_required
def create_post():
    """
    Create a new post.
    Args:
        Form Object: Consist of title, content, tags, image_url
        Image file: The image file to upload.
        image_url and image can not be provided at the same time.
    Returns:
        A JSON object containing the post's data and an HTTP status code.
    """
    try:
        postFormObj = request.form.to_dict()

        # Convert the 'tags' field back into an array
        if "tags" in postFormObj:
            postFormObj["tags"] = json.loads(postFormObj["tags"])

        image = request.files.get("image")

        createPostForm = CreatePostForm(formdata=MultiDict(postFormObj), image=image)
        createPostForm.set_tag_choices()

        if not createPostForm.validate_on_submit():
            errors_list = [
                error for errors in createPostForm.errors.values() for error in errors
            ]

            print(errors_list)

            return (
                jsonify(
                    {
                        "status": responseStatus.BAD_REQUEST,
                        "message": "Invalid form data",
                        "errors": errors_list,
                    }
                ),
                responseStatus.BAD_REQUEST,
            )

        image_url = postFormObj["image_url"] or None

        response = create_post_service(createPostForm, image_url)

        isSuccess = response.get("is_success")
        message = response.get("message")
        body = response.get("body", None)

        if not isSuccess or body is None:
            return error_message(message, responseStatus.BAD_REQUEST)

        postId = body["post_id"]

        return (
            jsonify(
                {
                    "status": responseStatus.OK,
                    "message": message,
                    "post_id": postId,
                }
            ),
            responseStatus.OK,
        )

    except Exception as e:
        print(e)
        return error_message(
            "Internal Server Error", responseStatus.INTERNAL_SERVER_ERROR
        )

#Retrieves a single post based on its ID, convert to DTO & return/error message
@api.route("/posts/<post_id>", methods=["GET"])
@api_login_required
def get_post(post_id):
    """
    Get a post by its ID.
    Args:
        post_id: The ID of the post to get.
        isPreview: A boolean indicating whether to return a preview of the post. Default is False.
    Returns:
        A JSON object containing the post's data and an HTTP status code.
    """
    try:
        isPreview = request.args.get("isPreview", "false").lower() == "true"
        post = Post.query.get(UUID(post_id))

        if post is None:
            return error_message("Post not found", responseStatus.NOT_FOUND)

        postDTO = PostDTO(post, post.postCreator, post.postCreator, isPreview).to_dict()

        return (
            jsonify({"status": responseStatus.OK, "post": postDTO}),
            responseStatus.OK,
        )

    except Exception as e:
        print(e)
        return error_message(
            "Internal Server Error", responseStatus.INTERNAL_SERVER_ERROR
        )


@api.route("/posts/<post_id>/post-status", methods=["PUT"])
@api_login_required
@api_is_admin
def edit_post_status(post_id):
    """
    Edit the post status by its ID. Note that only the admin can edit the post status. Note that only admin user can make this request.
    Args:
        post_id: The ID of the post to edit.
        postStatus: The new status of the post.
    Returns:
        A JSON object containing the post's data and an HTTP status code.
    """
    try:
        post_status = request.json.get("postStatus").upper()

        if post_status is None:
            return error_message(
                "Missing required parameter postStatus", responseStatus.BAD_REQUEST
            )

        if post_status not in [status.value.upper() for status in PostStatus]:
            return error_message("Invalid post status", responseStatus.BAD_REQUEST)

        post = Post.query.get(UUID(post_id))

        if post is None:
            return error_message("Post not found", responseStatus.NOT_FOUND)

        if post.status.value.upper() == post_status:
            return error_message(
                f"Post status is already in {post_status}", responseStatus.BAD_REQUEST
            )

        post.status = post_status
        post.updated_at = datetime.now()

        db.session.commit()

        return (
            jsonify(
                {"status": responseStatus.OK, "message": "Post edited successfully"}
            ),
            responseStatus.OK,
        )

    except Exception as e:
        db.session.rollback()
        print(e)
        return error_message(
            "Internal server error", responseStatus.INTERNAL_SERVER_ERROR
        )


@api.route("/posts/<post_id>", methods=["DELETE"])
@api_login_required
def delete_post(post_id):
    """
    Delete a post by its ID.
    Args:
        post_id: The ID of the post to delete.
        isSoftDelete: A boolean indicating whether to soft delete the post.
    Returns:
        A JSON object containing the post's data and an HTTP status code.
    """
    try:
        post = Post.query.get(UUID(post_id))
        isSoftDelete = request.json.get("isSoftDelete")
        user_id = current_user.id

        if isSoftDelete is None:
            return error_message(
                "Missing required parameter isSOftDelete", responseStatus.BAD_REQUEST
            )

        if post is None:
            return error_message("Post not found", responseStatus.NOT_FOUND)

        if user_id != post.user_id:
            return error_message(
                "User is not the owner of the post", responseStatus.UNAUTHORIZED
            )

        if isSoftDelete:
            if post.is_delete:
                return error_message(
                    "Post already soft deleted", responseStatus.BAD_REQUEST
                )
            post.is_delete = True
            post.updated_at = datetime.now()

        else:
            db.session.delete(post)

        db.session.commit()

        return (
            jsonify(
                {
                    "message": "Post deleted successfully",
                    "status": responseStatus.OK,
                }
            ),
            responseStatus.OK,
        )
    except Exception as e:
        db.session.rollback()
        print(e)
        return error_message(
            "Internal Server Error", responseStatus.INTERNAL_SERVER_ERROR
        )


@api.route("/posts/<post_id>/interactions", methods=["POST"])
@api_login_required
def post_interaction_handler(post_id):
    """
    Like a post by its ID.
    Args:
        post_id: The ID of the post.
        isLike: A boolean indicating whether to like the post. True means like, False means unlike.
        isBookmark: A boolean indicating whether to bookmark the post. True means bookmark, False means un-bookmark.
    Returns:
        A JSON object containing the post's id, operation flags (isLikeSuccess and isBookmarkSuccess) and an HTTP status code and a success message.
    """
    try:
        isLike = request.args.get("isLike")
        isBookmark = request.args.get("isBookmark")
        user_id = current_user.id

        if isLike is None and isBookmark is None:
            return error_message(
                "Missing required parameters, either isLike or isBookmark",
                responseStatus.BAD_REQUEST,
            )

        if isLike is not None:
            isLike = isLike.lower() == "true"

        if isBookmark is not None:
            isBookmark = isBookmark.lower() == "true"

        post = Post.query.get(UUID(post_id))

        if post is None:
            return error_message("Post not found", responseStatus.NOT_FOUND)

        isLikeSuccess = False
        isBookmarkSuccess = False

        if isinstance(isLike, bool):

            liked_post_query = select(PostLike).where(
                PostLike.c.post_id == post.id, PostLike.c.user_id == user_id
            )

            liked_post = db.session.execute(liked_post_query).fetchone()

            if liked_post is None:
                liked_post_insert_stmt = insert(PostLike).values(
                    post_id=post.id, user_id=user_id, created_at=datetime.now()
                )
                db.session.execute(liked_post_insert_stmt)
                isLikeSuccess = True
            else:
                liked_post_delete_stmt = delete(PostLike).where(
                    PostLike.c.post_id == post.id, PostLike.c.user_id == user_id
                )
                db.session.execute(liked_post_delete_stmt)
                isLikeSuccess = True

        db.session.commit()

        if isinstance(isBookmark, bool):
            isBookmarkSuccess = False

            bookmarked_post_query = select(PostBookmark).where(
                PostBookmark.c.post_id == post.id, PostBookmark.c.user_id == user_id
            )

            bookmarked_post = db.session.execute(bookmarked_post_query).fetchone()

            if bookmarked_post is None:
                bookmarked_post_insert_stmt = insert(PostBookmark).values(
                    post_id=post.id, user_id=user_id, created_at=datetime.now()
                )
                db.session.execute(bookmarked_post_insert_stmt)
                isBookmarkSuccess = True
            else:
                bookmarked_post_delete_stmt = delete(PostBookmark).where(
                    PostBookmark.c.post_id == post.id, PostBookmark.c.user_id == user_id
                )
                db.session.execute(bookmarked_post_delete_stmt)
                isBookmarkSuccess = True

        db.session.commit()

        return (
            jsonify(
                {
                    "status": responseStatus.OK,
                    "message": "Post interaction successful",
                    "isLike": "true" if isLikeSuccess else "false",
                    "isBookmark": "true" if isBookmarkSuccess else "false",
                    "post_id": post.id,
                },
            ),
            responseStatus.OK,
        )

    except Exception as e:
        db.session.rollback()
        print(e)
        return error_message(
            "Internal Server Error", responseStatus.INTERNAL_SERVER_ERROR
        )
