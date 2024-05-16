from flask import jsonify, request, render_template
from flask_login import current_user
from http import HTTPStatus as responseStatus

from . import api
from app.services.post_service import get_posts
from app.models import User
from app.utils.decorators import login_required
from app.utils.api_utils import error_message


@api.route("/paginate/postList", methods=["GET"])
@login_required
def get_post_list():
    """
    Get a list of posts based on infinite scrolling using server-side pagination.
    Args:
    page(int): The page number of the post list.
    per_page(int): The number of posts per page.
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
