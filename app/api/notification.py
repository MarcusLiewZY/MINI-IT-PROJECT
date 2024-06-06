from uuid import UUID
from flask import request, jsonify
from flask_login import current_user
from datetime import datetime
from http import HTTPStatus as responseStatus

from . import api
from app import db
from app.models import Post, PostNotification, CommentNotification, Comment, PostStatus
from app.services.notification_service import get_all_notifications
from app.utils.api_utils import error_message
from app.utils.decorators import api_login_required


@api.route("/notifications/count", methods=["GET"])
@api_login_required
def get_all_notification_count():
    """
    Get the count of all the notifications for the current user
    Args:
        None
    Returns:
        A response message with the count of all the notifications
    """
    try:
        notification_count, _ = get_all_notifications(current_user)
        return (
            jsonify(
                {
                    "status": responseStatus.OK,
                    "message": "Notification count retrieved successfully",
                    "notification_count": notification_count,
                }
            ),
            responseStatus.OK,
        )

    except Exception as e:
        print(e)
        return error_message(
            "Internal Server Error", responseStatus.INTERNAL_SERVER_ERROR
        )


@api.route("/notifications/<id>", methods=["PUT"])
@api_login_required
def update_notification(id):
    """
    Update the notification based on the notification type.
    Args:
        id: notification id (either post id, post notification id or comment notification id)
    Returns:
        A response message with the updated notification type, id and post detail url
    """
    try:
        data = request.json
        notification_type = data.get("type")
        notification_id = id

        if notification_type is None:
            return error_message(
                "Notification type is required", responseStatus.BAD_REQUEST
            )

        if notification_id is None:
            return error_message(
                "Notification id is required", responseStatus.BAD_REQUEST
            )

        notification_id = UUID(notification_id)

        if notification_type == "PostNotification":
            post_notification = PostNotification.query.filter(
                PostNotification.id == notification_id
            ).first()

            if post_notification is None:
                return error_message(
                    "Post notification not found", responseStatus.NOT_FOUND
                )

            # get the post id and the comment id from the post notification, then return the post detail page url
            post = Post.query.filter(Post.id == post_notification.post_id).first()

            if post is None:
                return error_message("Post not found", responseStatus.NOT_FOUND)

            post_id = post.id

            comment = Comment.query.filter(
                Comment.id == post_notification.unread_comment_id,
                Comment.post_id == post.id,
            ).first()

            if comment is None:
                return error_message("Comment not found", responseStatus.NOT_FOUND)

            comment_id = comment.id

            post_notification.is_read = True
            db.session.commit()

            post_detail_url = f"/posts/{post_id}#comment-{comment_id}"

            return (
                jsonify(
                    {
                        "status": responseStatus.OK,
                        "message": "Post notification updated successfully",
                        "post_detail_url": post_detail_url,
                        "notification_id": notification_id,
                        "notification_type": notification_type,
                    }
                ),
                responseStatus.OK,
            )

        elif notification_type == "CommentNotification":

            comment_notification = CommentNotification.query.filter(
                CommentNotification.id == notification_id,
            ).first()

            if comment_notification is None:
                return error_message(
                    "Comment notification not found", responseStatus.NOT_FOUND
                )

            comment = Comment.query.filter(
                Comment.id == comment_notification.comment_id
            ).first()

            if comment is None:
                return error_message("Comment not found", responseStatus.NOT_FOUND)

            reply = Comment.query.filter(
                Comment.id == comment_notification.unread_comment_id,
                Comment.replied_comment_id == comment.id,
            ).first()

            if reply is None:
                return error_message("Reply not found", responseStatus.NOT_FOUND)

            reply_id = reply.id
            post_id = reply.post_id

            comment_notification.is_read = True
            db.session.commit()

            post_detail_url = f"/posts/{post_id}#comment-{reply_id}"

            return jsonify(
                {
                    "status": responseStatus.OK,
                    "message": "Comment notification updated successfully",
                    "post_detail_url": post_detail_url,
                    "notification_id": notification_id,
                    "notification_type": notification_type,
                }
            )

        elif notification_type == "Post":
            post = Post.query.filter(Post.id == notification_id).first()

            if post is None:
                return error_message("Post not found", responseStatus.NOT_FOUND)

            if post.status == PostStatus.PENDING:
                pass
            elif (
                post.status == PostStatus.UNREAD_APPROVED
                or post.status == PostStatus.UNREAD_REJECTED
            ):
                if post.status == PostStatus.UNREAD_APPROVED:
                    post.status = PostStatus.APPROVED
                else:
                    post.status = PostStatus.REJECTED

                post.updated_at = datetime.now()
                db.session.commit()
            else:
                return error_message(
                    "Post status is not unread", responseStatus.BAD_REQUEST
                )

            post_detail_url = f"/posts/{post.id}"

            return jsonify(
                {
                    "status": responseStatus.OK,
                    "message": "Post status updated successfully",
                    "post_detail_url": post_detail_url,
                    "notification_id": notification_id,
                    "notification_type": notification_type,
                    "post_status": post.status.value,
                }
            )

        else:
            return error_message(
                "Invalid notification type", responseStatus.BAD_REQUEST
            )

    except Exception as e:
        db.session.rollback()
        print(e)
        return error_message(
            "Internal Server Error", responseStatus.INTERNAL_SERVER_ERROR
        )


@api.route(
    "/notifications/post-notifications/<post_notification_id>", methods=["DELETE"]
)
@api_login_required
def delete_post_notification(post_notification_id):
    """
    Permanent delete a post notification.
    Args:
        post_notification_id: the post notification id
    Returns:
    A JSON response with a message indicating the notification has been deleted and the notification id.
    """
    try:
        post_notification_id = UUID(post_notification_id)

        post_notification = PostNotification.query.filter(
            PostNotification.id == post_notification_id
        ).first()

        if post_notification is None:
            return error_message(
                "Post notification is not found", responseStatus.NOT_FOUND
            )

        db.session.delete(post_notification)
        db.session.commit()

        return (
            jsonify(
                {
                    "status": responseStatus.OK,
                    "message": "Post notification deleted successfully",
                    "post_notification_id": post_notification_id,
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


@api.route(
    "/notifications/comment-notifications/<comment_notification_id>", methods=["DELETE"]
)
@api_login_required
def delete_comment_notification(comment_notification_id):
    """
    Permanent delete a comment notification.
    Args:
    comment_notification_id: the comment notification id
    Returns:
    A JSON response with a message indicating the comment notification has been deleted and the comment notification id.
    """
    try:
        comment_notification_id = UUID(comment_notification_id)

        comment_notification = CommentNotification.query.filter(
            CommentNotification.id == comment_notification_id
        ).first()

        if comment_notification is None:
            return error_message(
                "Comment notification is not found", responseStatus.NOT_FOUND
            )

        db.session.delete(comment_notification)
        db.session.commit()

        return (
            jsonify(
                {
                    "status": responseStatus.OK,
                    "message": "Comment notification deleted successfully",
                    "comment_notification_id": comment_notification_id,
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


@api.route("/notifications/mark-all-as-read", methods=["PUT"])
@api_login_required
def mark_all_as_read_notifications():
    """
    Mark all as read notifications.
    Args:
        filter: filter the notifications by type: all, posts, comments, post-status
    Returns:
        A JSON response with a message indicating the notifications have been marked as read.
    """
    try:
        filter = request.args.get("filter")
        user_id = current_user.id

        if filter is None:
            return error_message(
                "Filter required parameter is missing", responseStatus.BAD_REQUEST
            )

        update_queries = {
            "post-notifications": lambda: PostNotification.query.filter(
                PostNotification.user_id == user_id,
                PostNotification.is_read == False,
            ).update({PostNotification.is_read: True}),
            "comment-notifications": lambda: CommentNotification.query.filter(
                CommentNotification.user_id == user_id,
                CommentNotification.is_read == False,
            ).update({CommentNotification.is_read: True}),
            "approved-posts": lambda: Post.query.filter(
                Post.user_id == user_id,
                Post.status == PostStatus.UNREAD_APPROVED,
                Post.is_delete == False,
            ).update(
                {
                    Post.status: PostStatus.APPROVED,
                    Post.updated_at: datetime.now(),
                }
            ),
            "rejected-posts": lambda: Post.query.filter(
                Post.user_id == user_id,
                Post.status == PostStatus.UNREAD_REJECTED,
                Post.is_delete == False,
            ).update(
                {
                    Post.status: PostStatus.UNREAD_REJECTED,
                    Post.updated_at: datetime.now(),
                }
            ),
        }

        if filter == "all":
            for update_query in update_queries.values():
                update_query()
        elif filter == "posts":
            update_queries["post-notifications"]()
        elif filter == "comments":
            update_queries["comment-notifications"]()
        elif filter == "post-status":
            update_queries["approved-posts"]()
            update_queries["rejected-posts"]()
        else:
            return error_message("Invalid filter", responseStatus.BAD_REQUEST)

        db.session.commit()

        return jsonify(
            {
                "status": responseStatus.OK,
                "message": f"{filter.capitalize()} marked as read successfully",
            }
        )

    except Exception as e:
        db.session.rollback()
        print(e)
        return error_message(
            "Internal Server Error", responseStatus.INTERNAL_SERVER_ERROR
        )
