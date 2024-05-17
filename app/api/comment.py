from uuid import UUID
from flask import request, jsonify
from datetime import datetime
from sqlalchemy import select, insert, delete
from http import HTTPStatus as responseStatus

from . import api
from app import db
from app.models import User, Comment, CommentLike, Post
from app.utils.helper import format_datetime
from app.utils.api_utils import error_message


@api.route("/comments", methods=["POST"])
def create_comment():
    """
    Create a comment for a post.
    Args:
        post_id: The ID of the post to comment on.
        user_id: The ID of the user who created the comment.
        content: The content of the comment.
    Returns:
        A JSON object containing the comment content and id with an HTTP status code.
    """

    try:
        content = request.json.get("comment")
        user_id = request.json.get("userId")
        post_id = request.json.get("postId")

        if content is None:
            return jsonify(
                {
                    "error": "Missing required parameters",
                    "status": responseStatus.BAD_REQUEST,
                },
                responseStatus.BAD_REQUEST,
            )
        elif content == "":
            return jsonify(
                {
                    "error": "Content cannot be empty",
                    "status": responseStatus.BAD_REQUEST,
                },
                responseStatus.BAD_REQUEST,
            )

        if user_id is None:
            return jsonify(
                {
                    "error": "Missing required user id parameter",
                    "status": responseStatus.BAD_REQUEST,
                },
                responseStatus.BAD_REQUEST,
            )

        if post_id is None:
            return jsonify(
                {
                    "error": "Missing required post id parameter",
                    "status": responseStatus.BAD_REQUEST,
                },
                responseStatus.BAD_REQUEST,
            )

        user = User.query.get(UUID(user_id))

        if user is None:
            return jsonify(
                {"error": "User not found", "status": responseStatus.NOT_FOUND},
                responseStatus.NOT_FOUND,
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

        comment.user_id = user.id
        comment.post_id = post.id

        db.session.add(comment)
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
        print(e)
        return (
            jsonify(
                {
                    "error": "Internal Server Error",
                    "status": responseStatus.INTERNAL_SERVER_ERROR,
                },
            ),
            responseStatus.INTERNAL_SERVER_ERROR,
        )


@api.route("/comments/<comment_id>", methods=["GET"])
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
def edit_comment(comment_id):
    """
    Edit a comment by its ID.
    Args:
        comment_id: The ID of the comment.
        userId: The ID of the comment creator.
        postId: The ID of the post the comment belongs to.
        content: The content of the comment.
    Returns:
        A JSON object containing the comment content and id with an http status code.
    """
    try:
        data = request.json
        user_id = data.get("userId")
        post_id = data.get("postId")
        content = data.get("comment")

        if user_id is None:
            return error_message(
                "Missing required user id parameter", responseStatus.BAD_REQUEST
            )

        if post_id is None:
            return error_message(
                "Missing required post id parameter", responseStatus.BAD_REQUEST
            )

        if content is None or content == "":
            return error_message("Content cannot be empty", responseStatus.BAD_REQUEST)

        user = User.query.get(UUID(user_id))
        post = Post.query.get(UUID(post_id))
        comment = Comment.query.get(UUID(comment_id))

        if user is None:
            return error_message("User not found", responseStatus.NOT_FOUND)

        if post is None:
            return error_message("Post not found", responseStatus.NOT_FOUND)

        if comment is None:
            return error_message("Comment not found", responseStatus.NOT_FOUND)

        if comment.user_id != user.id:
            return error_message("Unauthorized", responseStatus.UNAUTHORIZED)

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
        print(e)
        return (
            jsonify(
                {
                    "error": "Internal Server Error",
                    "status": responseStatus.INTERNAL_SERVER_ERROR,
                }
            ),
            responseStatus.INTERNAL_SERVER_ERROR,
        )


@api.route("/comments/<comment_id>", methods=["DELETE"])
def delete_comment(comment_id):
    """
    Delete a comment by its ID.
    Args:
        comment_id: The ID of the comment.
    Returns:
        A JSON object containing the comment's id and an HTTP status code.
    """

    try:
        comment = Comment.query.get(UUID(comment_id))
        print(comment)
        if comment is None:
            return jsonify(
                {
                    "status": responseStatus.NOT_FOUND,
                    "error": f"Comment with ID {comment_id} not found",
                },
                responseStatus.NOT_FOUND,
            )

        db.session.delete(comment)
        db.session.commit()

        return jsonify(
            {
                "status": responseStatus.NO_CONTENT,
                "message": "Comment deleted successfully",
                "comment_id": comment_id,
            },
            responseStatus.NO_CONTENT,
        )
    except Exception as e:
        print(e)
        return jsonify(
            {
                "error": "Internal Server Error",
                "status": responseStatus.INTERNAL_SERVER_ERROR,
            },
            responseStatus.INTERNAL_SERVER_ERROR,
        )


@api.route("/comments/<replied_comment_id>/reply", methods=["POST"])
def create_reply(replied_comment_id):
    """
    Create a reply to a comment.
    Args:
        replied_comment_id: The ID of the comment being replied to.
        user_id: The ID of the user who created the reply.
        post_id: The ID of the post the comment belongs to.
        content: The content of the reply.
    Returns:
        A JSON object containing the reply content and id with an HTTP status code.
    """
    try:
        user_id = request.json.get("userId")
        post_id = request.json.get("postId")
        content = request.json.get("comment")

        if user_id is None:
            return (
                jsonify(
                    {
                        "error": "Missing required user id parameter",
                        "status": responseStatus.BAD_REQUEST,
                    }
                ),
                responseStatus.BAD_REQUEST,
            )

        if post_id is None:
            return (
                jsonify(
                    {
                        "error": "Missing required post id parameter",
                        "status": responseStatus.BAD_REQUEST,
                    }
                ),
                responseStatus.BAD_REQUEST,
            )

        if content is None:
            return (
                jsonify(
                    {
                        "error": "Missing required content parameter",
                        "status": responseStatus.BAD_REQUEST,
                    }
                ),
                responseStatus.BAD_REQUEST,
            )

        if content == "":
            return (
                jsonify(
                    {
                        "error": "Content cannot be empty",
                        "status": responseStatus.BAD_REQUEST,
                    }
                ),
                responseStatus.BAD_REQUEST,
            )

        user = User.query.get(UUID(user_id))

        if user is None:
            return (
                jsonify(
                    {
                        "error": "User not found",
                        "status": responseStatus.NOT_FOUND,
                    }
                ),
                responseStatus.NOT_FOUND,
            )

        post = Post.query.get(UUID(post_id))

        if post is None:
            return (
                jsonify(
                    {
                        "error": "Post not found",
                        "status": responseStatus.NOT_FOUND,
                    }
                ),
                responseStatus.NOT_FOUND,
            )

        replied_comment = Comment.query.get(UUID(replied_comment_id))

        if replied_comment is None:
            return (
                jsonify(
                    {
                        "error": "Replied comment not found",
                        "status": responseStatus.NOT_FOUND,
                    }
                ),
                responseStatus.NOT_FOUND,
            )

        comment = Comment(
            {"content": content, "created_at": format_datetime(datetime.now())}
        )

        comment.user_id = user.id
        comment.post_id = post.id
        comment.replied_comment_id = replied_comment.id

        db.session.add(comment)
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
        print(e)
        return jsonify(
            {
                "error": "Internal Server Error",
                "status": responseStatus.INTERNAL_SERVER_ERROR,
            },
            responseStatus.INTERNAL_SERVER_ERROR,
        )


@api.route("/comments/<comment_id>", methods=["POST"])
def comment_interaction_handler(comment_id):
    """
    Like a post by its ID.
    Args:
        comment_id: The ID of the comment.
        user_id: The ID of the user who react to the comment.
        isLike: A boolean indicating whether to like the comment. True means like, False means unlike.
    Returns:
        A JSON object containing the post's id and an HTTP status code and a success message.
    """
    try:
        isLike = request.args.get("isLike")
        user_id = request.json.get("userId")

        if isLike is None:
            return (
                jsonify({"error": "Missing required parameters, isLike"}),
                responseStatus.BAD_REQUEST,
            )

        if isLike is not None:
            isLike = isLike.lower() == "true"

        comment = Comment.query.get(UUID(comment_id))
        user = User.query.get(UUID(user_id))

        if comment is None:
            return (jsonify({"error": "Comment not found"}), responseStatus.NOT_FOUND)

        if user is None:
            return (jsonify({"error": "User not found"}), responseStatus.NOT_FOUND)

        isLikeSuccess = False

        if isinstance(isLike, bool):
            liked_comment_query = select(CommentLike).where(
                CommentLike.c.comment_id == comment.id, CommentLike.c.user_id == user.id
            )

            liked_comment = db.session.execute(liked_comment_query).fetchone()
            if liked_comment is None:
                liked_comment_insert_stmt = insert(CommentLike).values(
                    comment_id=comment.id,
                    user_id=user.id,
                )
                db.session.execute(liked_comment_insert_stmt)
                isLikeSuccess = True
            else:
                liked_comment_delete_stmt = delete(CommentLike).where(
                    CommentLike.c.comment_id == comment.id,
                    CommentLike.c.user_id == user.id,
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
        )

    except Exception as e:
        print(e)
        return (
            jsonify({"error": "Internal Server Error"}),
            responseStatus.INTERNAL_SERVER_ERROR,
        )
