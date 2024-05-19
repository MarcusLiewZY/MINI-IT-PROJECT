from datetime import datetime
from uuid import UUID
from sqlalchemy import select, insert, delete
from flask import jsonify, request
from http import HTTPStatus as responseStatus

from . import api
from app import db
from app.models import User, PostLike, PostBookmark
from app.models.post import Post, Status
from app.dto.post_dto import PostDTO
from app.utils.helper import format_datetime


@api.route("/posts", methods=["GET"])
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
                Post.status.in_[Status.APPROVED, Status.UNREAD_APPROVED]
            )

        posts = query.order_by(Post.updated_at.desc()).all()
        postDTOs = [
            PostDTO(post, post.postCreator, post.postCreator, isPreview).to_dict()
            for post in posts
        ]

        return jsonify({"posts": postDTOs}), responseStatus.OK

    except Exception as e:
        print(e)
        return (
            jsonify({"error": "Internal Server Error"}),
            responseStatus.INTERNAL_SERVER_ERROR,
        )


@api.route("/posts/<post_id>", methods=["GET"])
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
            return (
                jsonify({"error": "Post not found"}),
                responseStatus.NOT_FOUND,
            )

        postDTO = PostDTO(post, post.postCreator, post.postCreator, isPreview).to_dict()

        return jsonify({"post": postDTO}), responseStatus.OK
    except Exception as e:
        print(e)
        return (
            jsonify({"error": "Internal Server Error"}),
            responseStatus.INTERNAL_SERVER_ERROR,
        )


@api.route("/posts/<post_id>", methods=["DELETE"])
def delete_post(post_id):
    """
    Delete a post by its ID.
    Args:
        post_id: The ID of the post to delete.
        isSoftDelete: A boolean indicating whether to soft delete the post.
        user_id: The ID of the user who is deleting the post.
    Returns:
        A JSON object containing the post's data and an HTTP status code.
    """
    try:
        post = Post.query.get(UUID(post_id))
        isSoftDelete = request.json.get("isSoftDelete")
        user_id = request.json.get("userId")

        if user_id is None:
            return (
                jsonify({"error": "Post already soft deleted"}),
                responseStatus.BAD_REQUEST,
            )

        if isSoftDelete is None:
            return (
                jsonify({"error": "Missing required parameter isSoftDelete"}),
                responseStatus.BAD_REQUEST,
            )

        if post is None:
            return (
                jsonify({"error": "Post not found"}),
                responseStatus.NOT_FOUND,
            )

        print(user_id, post.user_id)
        print(type(user_id), type(post.user_id))
        print(user_id != post.user_id)

        if UUID(user_id) != post.user_id:
            return (
                jsonify({"error": "User is not the owner of the post"}),
                responseStatus.UNAUTHORIZED,
            )

        if isSoftDelete:
            if post.is_delete:
                return (
                    jsonify({"error": "Post already soft deleted"}),
                    responseStatus.BAD_REQUEST,
                )
            post.is_delete = True
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
        print(e)
        return (
            jsonify({"error": "Internal Server Error"}),
            responseStatus.INTERNAL_SERVER_ERROR,
        )


@api.route("/posts/<post_id>/<user_id>", methods=["POST"])
def post_interaction_handler(post_id, user_id):
    """
    Like a post by its ID.
    Args:
        post_id: The ID of the post.
        user_id: The ID of the user who react the post.
        isLike: A boolean indicating whether to like the post. True means like, False means unlike.
        isBookmark: A boolean indicating whether to bookmark the post. True means bookmark, False means un-bookmark.
    Returns:
        A JSON object containing the post's id, operation flags (isLikeSuccess and isBookmarkSuccess) and an HTTP status code and a success message.
    """
    try:
        isLike = request.args.get("isLike")
        isBookmark = request.args.get("isBookmark")

        if isLike is None and isBookmark is None:
            return (
                jsonify(
                    {
                        "error": "Missing required parameters, either isLike or isBookmark"
                    }
                ),
                responseStatus.BAD_REQUEST,
            )

        if isLike is not None:
            isLike = isLike.lower() == "true"

        if isBookmark is not None:
            isBookmark = isBookmark.lower() == "true"

        post = Post.query.get(UUID(post_id))
        user = User.query.get(UUID(user_id))

        if post is None:
            return (jsonify({"error": "Post not found"}), responseStatus.NOT_FOUND)

        if user is None:
            return (jsonify({"error": "User not found"}), responseStatus.NOT_FOUND)

        isLikeSuccess = False
        isBookmarkSuccess = False

        if isinstance(isLike, bool):

            liked_post_query = select(PostLike).where(
                PostLike.c.post_id == post.id, PostLike.c.user_id == user.id
            )

            liked_post = db.session.execute(liked_post_query).fetchone()

            if liked_post is None:
                liked_post_insert_stmt = insert(PostLike).values(
                    post_id=post.id,
                    user_id=user.id,
                    created_at=format_datetime(datetime.now()),
                )
                db.session.execute(liked_post_insert_stmt)
                isLikeSuccess = True
            else:
                liked_post_delete_stmt = delete(PostLike).where(
                    PostLike.c.post_id == post.id, PostLike.c.user_id == user.id
                )
                db.session.execute(liked_post_delete_stmt)
                isLikeSuccess = True

        db.session.commit()

        if isinstance(isBookmark, bool):
            isBookmarkSuccess = False

            bookmarked_post_query = select(PostBookmark).where(
                PostBookmark.c.post_id == post.id, PostBookmark.c.user_id == user.id
            )

            bookmarked_post = db.session.execute(bookmarked_post_query).fetchone()

            if bookmarked_post is None:
                bookmarked_post_insert_stmt = insert(PostBookmark).values(
                    post_id=post.id,
                    user_id=user.id,
                    created_at=format_datetime(datetime.now()),
                )
                db.session.execute(bookmarked_post_insert_stmt)
                isBookmarkSuccess = True
            else:
                bookmarked_post_delete_stmt = delete(PostBookmark).where(
                    PostBookmark.c.post_id == post.id, PostBookmark.c.user_id == user.id
                )
                db.session.execute(bookmarked_post_delete_stmt)
                isBookmarkSuccess = True

        db.session.commit()

        return jsonify(
            {
                "status": responseStatus.OK,
                "message": "Post interaction successful",
                "isLike": "true" if isLikeSuccess else "false",
                "isBookmark": "true" if isBookmarkSuccess else "false",
                "post_id": post.id,
            },
            # responseStatus.OK
        )

    except Exception as e:
        print(e)
        return (
            jsonify({"error": "Internal Server Error"}),
            responseStatus.INTERNAL_SERVER_ERROR,
        )
