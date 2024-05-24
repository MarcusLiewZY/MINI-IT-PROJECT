from uuid import UUID
from flask import request, jsonify
from flask_login import current_user
from datetime import datetime
from sqlalchemy import select, insert, delete
from http import HTTPStatus as responseStatus

from . import api
from app import db
from app.models import (
    User,
    Comment,
    CommentLike,
    Post,
    PostNotification,
    CommentNotification,
)
from app.utils.helper import format_datetime
from app.utils.api_utils import error_message
from app.utils.decorators import api_login_required


@api.route("/comments", methods=["POST"])
@api_login_required
def create_comment():
    """
    Create a comment and post notification for a post.
    Args:
        post_id: The ID of the post to comment on.
        content: The content of the comment.
    Returns:
        A JSON object containing the comment content and id with an HTTP status code.
    """

    try:
        content = request.json.get("comment")
        post_id = request.json.get("postId")
        user_id = current_user.id

        if content is None:
            return error_message(
                "Missing required content parameter", responseStatus.BAD_REQUEST
            )
        elif content == "":
            return error_message("Content cannot be empty", responseStatus.BAD_REQUEST)

        if post_id is None:
            return error_message(
                "Missing required post id parameter", responseStatus.BAD_REQUEST
            )

        post = Post.query.get(UUID(post_id))

        if post is None:
            return jsonify(
                {"error": "Post not found", "status": responseStatus.NOT_FOUND},
                responseStatus.NOT_FOUND,
            )

        comment = Comment(
            {"content": content, "created_at": format_datetime(datetime.now())}
        )

        comment.user_id = user_id
        comment.post_id = post.id

        db.session.add(comment)
        db.session.commit()

        post_notification = PostNotification(
            {
                "user_id": post.user_id,
                "post_id": post.id,
                "unread_comment_id": comment.id,
                "created_at": format_datetime(datetime.now()),
            }
        )

        db.session.add(post_notification)
        db.session.commit()

        return (
            jsonify(
                {
                    "status": responseStatus.CREATED,
                    "message": "Comment created successfully",
                    "comment_id": comment.id,
                    "content": comment.content,
                },
            ),
            responseStatus.CREATED,
        )

    except Exception as e:
        db.session.rollback()
        print(e)
        return error_message(
            "Internal Server Error", responseStatus.INTERNAL_SERVER_ERROR
        )


@api.route("/comments/<comment_id>", methods=["GET"])
@api_login_required
def get_comment(comment_id):
    """
    Get a comment by its ID.
    Args:
        comment_id: The ID of the comment.
    Returns:
        A JSON object containing the comment content and id with an HTTP status code.
    """
    try:
        comment = Comment.query.get(UUID(comment_id))

        if comment is None:
            return error_message("Comment not found", responseStatus.NOT_FOUND)

        return (
            jsonify(
                {
                    "status": responseStatus.OK,
                    "comment_id": comment.id,
                    "content": comment.content,
                }
            ),
            responseStatus.OK,
        )

    except Exception as e:
        print(e)
        return error_message(
            "Internal Server Error", responseStatus.INTERNAL_SERVER_ERROR
        )


@api.route("/comments/<comment_id>", methods=["PUT"])
@api_login_required
def edit_comment(comment_id):
    """
    Edit a comment by its ID.
    Args:
        comment_id: The ID of the comment.
        postId: The ID of the post the comment belongs to.
        content: The content of the comment.
    Returns:
        A JSON object containing the comment content and id with an http status code.
    """
    try:
        data = request.json
        post_id = data.get("postId")
        content = data.get("comment")
        user_id = current_user.id

        if post_id is None:
            return error_message(
                "Missing required post id parameter", responseStatus.BAD_REQUEST
            )

        if content is None or content == "":
            return error_message("Content cannot be empty", responseStatus.BAD_REQUEST)

        post = Post.query.get(UUID(post_id))
        comment = Comment.query.get(UUID(comment_id))

        if post is None:
            return error_message("Post not found", responseStatus.NOT_FOUND)

        if comment is None:
            return error_message("Comment not found", responseStatus.NOT_FOUND)

        if comment.user_id != user_id:
            return error_message(
                "This comment is not belong to logged in user",
                responseStatus.UNAUTHORIZED,
            )

        if comment.post_id != post.id:
            return error_message(
                "Post does not match the comment", responseStatus.BAD_REQUEST
            )

        comment.content = content
        comment.updated_at = format_datetime(datetime.now())

        db.session.commit()

        return (
            jsonify(
                {
                    "status": responseStatus.OK,
                    "message": "Comment updated successfully",
                    "comment_id": comment.id,
                    "content": comment.content,
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


@api.route("/comments/<comment_id>", methods=["DELETE"])
@api_login_required
def delete_comment(comment_id):
    """
    Delete a comment by its ID.
    Args:
        comment_id: The ID of the comment.
    Returns:
        A JSON object containing the comment's id and an HTTP status code.
    """

    try:
        user_id = current_user.id

        comment = Comment.query.get(UUID(comment_id))

        if comment is None:
            return error_message("Comment not found", responseStatus.NOT_FOUND)

        if not current_user.is_admin and comment.user_id != user_id:
            return error_message("Unauthorized", responseStatus.UNAUTHORIZED)

        db.session.delete(comment)
        db.session.commit()

        return (
            jsonify(
                {
                    "status": responseStatus.OK,
                    "message": "Comment deleted successfully",
                    "comment_id": comment_id,
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


@api.route("/comments/<replied_comment_id>/reply", methods=["POST"])
@api_login_required
def create_reply(replied_comment_id):
    """
    Create a reply and the comment notification for the comment.
    Args:
        replied_comment_id: The ID of the comment being replied to.
        post_id: The ID of the post the comment belongs to.
        content: The content of the reply.
    Returns:
        A JSON object containing the reply content and id with an HTTP status code.
    """
    try:
        user_id = current_user.id
        post_id = request.json.get("postId")
        content = request.json.get("comment")

        if post_id is None:
            return error_message(
                "Missing required post id parameter", responseStatus.BAD_REQUEST
            )

        if content is None:
            return error_message(
                "Missing required content parameter", responseStatus.BAD_REQUEST
            )

        if content == "":
            return error_message("Content cannot be empty", responseStatus.BAD_REQUEST)

        post = Post.query.get(UUID(post_id))

        if post is None:
            return error_message("Post not found", responseStatus.NOT_FOUND)

        replied_comment = Comment.query.get(UUID(replied_comment_id))

        if replied_comment is None:
            return error_message("Replied comment not found", responseStatus.NOT_FOUND)

        comment = Comment(
            {"content": content, "created_at": format_datetime(datetime.now())}
        )

        comment.user_id = user_id
        comment.post_id = post.id
        comment.replied_comment_id = replied_comment.id

        db.session.add(comment)
        db.session.commit()

        comment_notification = CommentNotification(
            {
                "user_id": replied_comment.user_id,
                "comment_id": replied_comment.id,
                "unread_comment_id": comment.id,
                "created_at": format_datetime(datetime.now()),
            }
        )

        db.session.add(comment_notification)
        db.session.commit()

        return (
            jsonify(
                {
                    "status": responseStatus.CREATED,
                    "message": "Reply created successfully",
                    "comment_id": comment.id,
                    "content": comment.content,
                    "replied_comment_id": replied_comment.id,
                    "comment_user_anon_no": comment.commentCreator.anon_no,
                    "replied_comment_user_anon_no": replied_comment.commentCreator.anon_no,
                }
            ),
            responseStatus.CREATED,
        )

    except Exception as e:
        db.session.rollback()
        print(e)
        return jsonify(
            {
                "error": "Internal Server Error",
                "status": responseStatus.INTERNAL_SERVER_ERROR,
            },
            responseStatus.INTERNAL_SERVER_ERROR,
        )


@api.route("/comments/<comment_id>", methods=["POST"])
@api_login_required
def comment_interaction_handler(comment_id):
    """
    Like a post by its ID.
    Args:
        comment_id: The ID of the comment.
        isLike: A boolean indicating whether to like the comment. True means like, False means unlike.
    Returns:
        A JSON object containing the post's id and an HTTP status code and a success message.
    """
    try:
        isLike = request.args.get("isLike")
        user_id = current_user.id

        if isLike is None:
            return (
                jsonify({"error": "Missing required parameters, isLike"}),
                responseStatus.BAD_REQUEST,
            )

        if isLike is not None:
            isLike = isLike.lower() == "true"

        comment = Comment.query.get(UUID(comment_id))

        if comment is None:
            return error_message("Comment not found", responseStatus.NOT_FOUND)

        isLikeSuccess = False

        if isinstance(isLike, bool):
            liked_comment_query = select(CommentLike).where(
                CommentLike.c.comment_id == comment.id, CommentLike.c.user_id == user_id
            )

            liked_comment = db.session.execute(liked_comment_query).fetchone()
            if liked_comment is None:
                liked_comment_insert_stmt = insert(CommentLike).values(
                    comment_id=comment.id,
                    user_id=user_id,
                )
                db.session.execute(liked_comment_insert_stmt)
                isLikeSuccess = True
            else:
                liked_comment_delete_stmt = delete(CommentLike).where(
                    CommentLike.c.comment_id == comment.id,
                    CommentLike.c.user_id == user_id,
                )
                db.session.execute(liked_comment_delete_stmt)
                isLikeSuccess = True

        db.session.commit()

        return jsonify(
            {
                "status": responseStatus.OK,
                "message": "Comment interaction successful",
                "isLike": "true" if isLikeSuccess else "false",
                "comment_id": comment.id,
            },
            responseStatus.OK,
        )

    except Exception as e:
        db.session.rollback()
        print(e)
        return error_message(
            "Internal Server Error", responseStatus.INTERNAL_SERVER_ERROR
        )


@api.route("/comments/<comment_id>/reporting", methods=["PUT"])
@api_login_required
def report_comment(comment_id):
    """
    Report a comment by its ID.
    Args:
    comment_id: The ID of the comment.
    isReport: A boolean indicating whether to report the comment. True means report, False means cancel report.
    Returns:
    A JSON object containing the comment's id and an HTTP status code and a success message.

    """
    try:
        user_id = current_user.id
        isReport = request.args.get("isReport")

        if isReport is None:
            return error_message(
                "Missing required isReport parameter", responseStatus.BAD_REQUEST
            )

        comment = Comment.query.get(UUID(comment_id))

        if comment is None:
            return error_message("Comment not found", responseStatus.NOT_FOUND)

        if isReport == "true":
            if comment.is_report is True:
                return error_message(
                    "Comment already reported", responseStatus.BAD_REQUEST
                )

            comment.is_report = True

        elif isReport == "false":
            if comment.is_report is False:
                return error_message(
                    "Comment already cancel reported", responseStatus.BAD_REQUEST
                )

            if current_user.is_admin is False:
                return error_message(
                    "Unauthorized with admin role", responseStatus.UNAUTHORIZED
                )

            comment.is_report = False

        else:
            return error_message(
                "Invalid isReport parameter", responseStatus.BAD_REQUEST
            )

        db.session.commit()

        return (
            jsonify(
                {
                    "status": responseStatus.OK,
                    "message": f"Comment is {'cancel' if not comment.is_report else ''} reported successful",
                    "comment_id": comment.id,
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
