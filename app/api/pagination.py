from flask import jsonify, request, render_template
from flask_login import current_user
from http import HTTPStatus as responseStatus

from . import api
from app.services.post_service import (
    get_posts,
    get_created_posts,
    get_liked_posts,
    get_replies_posts,
    get_bookmarked_posts,
    get_rejected_posts,
)
from app.services.notification_service import (
    get_paginate_post_notifications,
    get_paginate_comment_notifications,
    get_paginate_posts,
    get_paginate_all_notifications,
)
from app.services.admin_service import (
    get_paginate_reporting_comments,
    get_paginate_approving_post,
    get_paginate_all_admin_notifications,
)
from app.services.search_service import PostSearchEngine
from app.models import User
from app.utils.decorators import api_login_required
from app.utils.api_utils import error_message


@api.route("/paginate/post-list", methods=["GET"])
@api_login_required
def get_post_list():
    """
    Get a list of posts based on infinite scrolling using server-side pagination.
    Args:
    page(int): The page number of the post list.
    per_page(int): The number of the posts per page.
    Returns:
    A JSON response containing the status, message, page, per_page, and the rendered post list.
    """
    try:

        page = request.args.get("page", 1, type=int)
        per_page = request.args.get("per_page", 5, type=int)

        user = User.query.get(current_user.id)
        has_next, postDTOs = get_posts(
            user, isPreview=True, page=page, per_page=per_page
        )

        rendered_postList = render_template(
            "layouts/postCardList.html", posts=postDTOs, user=user
        )

        return (
            jsonify(
                {
                    "status": responseStatus.OK,
                    "message": "Post list retrieved successfully",
                    "page": page,
                    "per_page": per_page,
                    "has_next": has_next,
                    "html": rendered_postList,
                },
            ),
            responseStatus.OK,
        )

    except Exception as e:
        print(e)
        return error_message(
            "Internal server error", responseStatus.INTERNAL_SERVER_ERROR
        )


@api.route("/paginate/search-post-list", methods=["GET"])
def get_searched_post_list():
    """
    Get a list of searched posts based on infinite scrolling using server-side pagination.
    Args:
    search_text(str): The search text to search for.
    updated_time_filter(str): The updated time filter to filter the posts.
    type_filter(str): The type filter to filter the posts.
    tag_filter(str): The tag filter to filter the posts.
    sort_by(str): The sort by filter to sort the posts.
    page(int): The page number of the post list.
    per_page(int): The number of the posts per page.
    Returns:
    A JSON response containing the status, message, page, per_page, and the rendered post list.
    """
    try:

        searchArgs = request.args

        search_text = searchArgs.get("search_text", None, type=str)
        updated_time_filter = searchArgs.get("updated_time_filter", None, type=str)
        type_filter = searchArgs.get("type_filter", None, type=str)
        tag_filter = searchArgs.getlist("tag_filter", None)
        sort_by = searchArgs.get("sort_by", None, type=str)
        page = searchArgs.get("page", 1, type=int)
        per_page = searchArgs.get("per_page", 5, type=int)

        search_dist = {
            "search_text": search_text,
            "updated_time_filter": updated_time_filter,
            "type_filter": type_filter,
            "tag_filter": tag_filter,
            "sort_by": sort_by,
        }

        search_engine = PostSearchEngine()
        has_next, postDTOs = search_engine.search_posts(
            user=current_user,
            isPreview=True,
            page=page,
            per_page=per_page,
            search_dist=search_dist,
        )

        rendered_postList = render_template(
            "layouts/postCardList.html", posts=postDTOs, user=current_user
        )

        return (
            jsonify(
                {
                    "status": responseStatus.OK,
                    "message": "Searched post list retrieved successfully",
                    "page": page,
                    "per_page": per_page,
                    "has_next": has_next,
                    "html": rendered_postList,
                }
            ),
            responseStatus.OK,
        )

    except Exception as e:
        print(e)
        return error_message(
            "Internal server error", responseStatus.INTERNAL_SERVER_ERROR
        )


@api.route("/paginate/me/created-post-list", methods=["GET"])
@api_login_required
def get_created_post_list():
    """
    Get a list of created posts based on infinite scrolling using server-side pagination.
    Args:
    page(int): The page number of the post list.
    per_page(int): The number of the posts per page.
    Returns:
    A JSON response containing the status, message, page, per_page, and the rendered post list.
    """
    try:
        page = request.args.get("page", 1, type=int)
        per_page = request.args.get("per_page", 5, type=int)

        user = User.query.get(current_user.id)
        has_next, postDTOs = get_created_posts(
            user, isPreview=True, page=page, per_page=per_page
        )

        rendered_postList = render_template(
            "layouts/postCardList.html", posts=postDTOs, user=user
        )

        return (
            jsonify(
                {
                    "status": responseStatus.OK,
                    "message": "Created post list retrieved successfully",
                    "page": page,
                    "per_page": per_page,
                    "has_next": has_next,
                    "html": rendered_postList,
                }
            ),
            responseStatus.OK,
        )

    except Exception as e:
        print(e)
        return error_message(
            "Internal server error", responseStatus.INTERNAL_SERVER_ERROR
        )


@api.route("/paginate/me/liked-post-list", methods=["GET"])
@api_login_required
def get_liked_post_list():
    """
    Get a list of liked posts based on infinite scrolling using server-side pagination.
    Args:
    page(int): The page number of the post list.
    per_page(int): The number of the posts per page.
    Returns:
    A JSON response containing the status, message, page, per_page, and the rendered post list.
    """
    try:
        page = request.args.get("page", 1, type=int)
        per_page = request.args.get("per_page", 5, type=int)

        user = User.query.get(current_user.id)
        has_next, postDTOs = get_liked_posts(
            user, isPreview=True, page=page, per_page=per_page
        )

        rendered_postList = render_template(
            "layouts/postCardList.html", posts=postDTOs, user=user
        )

        return (
            jsonify(
                {
                    "status": responseStatus.OK,
                    "message": "Liked post list retrieved successfully",
                    "page": page,
                    "per_page": per_page,
                    "has_next": has_next,
                    "html": rendered_postList,
                }
            ),
            responseStatus.OK,
        )

    except Exception as e:
        print(e)
        return error_message(
            "Internal server error", responseStatus.INTERNAL_SERVER_ERROR
        )


@api.route("/paginate/me/replies-post-list", methods=["GET"])
@api_login_required
def get_replies_post_list():
    """
    Get a list of replied posts based on infinite scrolling using server-side pagination.
    Args:
    page(int): The page number of the post list.
    per_page(int): The number of the posts per page.
    Returns:
    A JSON response containing the status, message, page, per_page, and the rendered post list.
    """
    try:
        page = request.args.get("page", 1, type=int)
        per_page = request.args.get("per_page", 5, type=int)

        user = User.query.get(current_user.id)
        has_next, postDTOs = get_replies_posts(
            user, isPreview=True, page=page, per_page=per_page
        )

        rendered_postList = render_template(
            "layouts/postCardList.html", posts=postDTOs, user=user
        )

        return (
            jsonify(
                {
                    "status": responseStatus.OK,
                    "message": "Liked post list retrieved successfully",
                    "page": page,
                    "per_page": per_page,
                    "has_next": has_next,
                    "html": rendered_postList,
                }
            ),
            responseStatus.OK,
        )

    except Exception as e:
        print(e)
        return error_message(
            "Internal server error", responseStatus.INTERNAL_SERVER_ERROR
        )


@api.route("/paginate/me/bookmarked-post-list", methods=["GET"])
@api_login_required
def get_bookmarked_post_list():
    """
    Get a list of bookmarked posts based on infinite scrolling using server-side pagination.
    Args:
    page(int): The page number of the post list.
    per_page(int): The number of the posts per page.
    Returns:
    A JSON response containing the status, message, page, per_page, and the rendered post list.
    """
    try:
        page = request.args.get("page", 1, type=int)
        per_page = request.args.get("per_page", 5, type=int)

        user = User.query.get(current_user.id)
        has_next, postDTOs = get_bookmarked_posts(
            user, isPreview=True, page=page, per_page=per_page
        )

        rendered_postList = render_template(
            "layouts/postCardList.html", posts=postDTOs, user=user
        )

        return (
            jsonify(
                {
                    "status": responseStatus.OK,
                    "message": "Liked post list retrieved successfully",
                    "page": page,
                    "per_page": per_page,
                    "has_next": has_next,
                    "html": rendered_postList,
                }
            ),
            responseStatus.OK,
        )

    except Exception as e:
        print(e)
        return error_message(
            "Internal server error", responseStatus.INTERNAL_SERVER_ERROR
        )


@api.route("/paginate/me/rejected-post-list", methods=["GET"])
@api_login_required
def get_rejected_post_list():
    """
    Get a list of rejected posts based on infinite scrolling using server-side pagination.
    Args:
    page(int): The page number of the rejected post list.
    per_page(int): The number of the posts per page.
    Returns:
    A JSON response containing the status, message, page, per_page, and the rendered post list
    """
    try:
        page = request.args.get("page", 1, type=int)
        per_page = request.args.get("per_page", 1, type=int)

        user = User.query.get(current_user.id)
        has_next, postDTOs = get_rejected_posts(
            user, isPreview=True, page=page, per_page=per_page
        )

        rendered_postList = render_template(
            "layouts/postCardList.html", posts=postDTOs, user=user
        )

        return (
            jsonify(
                {
                    "status": responseStatus.OK,
                    "message": "Rejected post list retrieved successfully",
                    "page": page,
                    "per_page": per_page,
                    "has_next": has_next,
                    "html": rendered_postList,
                }
            ),
            responseStatus.OK,
        )

    except Exception as e:
        print(e)
        return error_message(
            "Internal Server Error", responseStatus.INTERNAL_SERVER_ERROR
        )


@api.route("/paginate/notification", methods=["GET"])
@api_login_required
def get_notification_list():
    """
    Get a list of notifications based on infinite scrolling using server-side pagination.
    Args:
    filter(str): The type of notification to filter.
    page(int): The page number of the post list.
    per_page(int): The number of the posts per page.
    Returns:
    A JSON response containing the status, message, page, per_page, and the rendered post list.
    """
    try:
        filter = request.args.get("filter", "all", type=str)
        page = request.args.get("page", 1, type=int)
        per_page = request.args.get("per_page", 5, type=int)

        user = User.query.get(current_user.id)
        notificationDTOs = []
        has_next = False

        if filter == "all":
            has_next, notificationDTOs = get_paginate_all_notifications(
                user, page=page, per_page=per_page
            )
        elif filter == "posts":
            has_next, notificationDTOs = get_paginate_post_notifications(
                user, page=page, per_page=per_page
            )
        elif filter == "comments":
            has_next, notificationDTOs = get_paginate_comment_notifications(
                user, page=page, per_page=per_page
            )
        elif filter == "post-status":
            has_next, notificationDTOs = get_paginate_posts(
                user, page=page, per_page=per_page
            )
        else:
            return error_message("Invalid filter type", responseStatus.BAD_REQUEST)

        rendered_notifications = render_template(
            "notifications/notificationList.html",
            notifications=notificationDTOs,
            user=user,
        )

        return (
            jsonify(
                {
                    "status": responseStatus.OK,
                    "message": "Notification list retrieved successfully",
                    "page": page,
                    "per_page": per_page,
                    "has_next": has_next,
                    "html": rendered_notifications,
                }
            ),
            responseStatus.OK,
        )

    except Exception as e:
        print(e)
        return error_message(
            "Internal server error", responseStatus.INTERNAL_SERVER_ERROR
        )


@api.route("/paginate/admin-notification", methods=["GET"])
def get_admin_notification_list():
    """
    Get a list of admin notifications based on infinite scrolling using server-side pagination.
    Args:
    filter(str): The type of notification to filter.
    page(int): The page number of the post list.
    per_page(int): The number of the posts per page.
    Returns:
    A JSON response containing the status, message, page, per_page, and the rendered post list.
    """
    try:
        filter = request.args.get("filter", "all", type=str)
        page = request.args.get("page", 1, type=int)
        per_page = request.args.get("per_page", 5, type=int)

        adminNotificationDTOs = []
        has_next = False

        if filter == "all":
            has_next, adminNotificationDTOs = get_paginate_all_admin_notifications(
                page=page, per_page=per_page
            )
        elif filter == "reporting-comments":
            has_next, adminNotificationDTOs = get_paginate_reporting_comments(
                page=page, per_page=per_page
            )
        elif filter == "approving-posts":
            has_next, adminNotificationDTOs = get_paginate_approving_post(
                page=page, per_page=per_page
            )
        else:
            return error_message("Invalid filter type", responseStatus.BAD_REQUEST)

        rendered_admin_notifications = render_template(
            "admin/adminList.html",
            adminNotifications=adminNotificationDTOs,
        )

        return (
            jsonify(
                {
                    "status": responseStatus.OK,
                    "message": "Admin notification list retrieved successfully",
                    "page": page,
                    "per_page": per_page,
                    "has_next": has_next,
                    "html": rendered_admin_notifications,
                }
            ),
            responseStatus.OK,
        )

    except Exception as e:
        print(e)
        return error_message(
            "Internal server error", responseStatus.INTERNAL_SERVER_ERROR
        )
