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
)
from app.models import User
from app.utils.decorators import login_required
from app.utils.api_utils import error_message


@api.route("/paginate/post-list", methods=["GET"])
@login_required
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


@api.route("/paginate/created-post-list", methods=["GET"])
@login_required
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


@api.route("/paginate/liked-post-list", methods=["GET"])
@login_required
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


@api.route("/paginate/replies-post-list", methods=["GET"])
@login_required
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


@api.route("/paginate/bookmarked-post-list", methods=["GET"])
@login_required
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
