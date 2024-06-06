from uuid import UUID
from flask import flash, redirect, url_for, render_template
from flask_login import current_user

from . import post
from app.models.post import Post, PostStatus
from app.models.user import User
from app.models.tag import Tag
from app.dto.post_dto import PostDTO
from app.utils.decorators import login_required, require_accept_community_guideline


@post.route("/<post_id>", methods=["GET"])
@login_required
@require_accept_community_guideline
def get_post(post_id):

    user = User.query.get(current_user.id)
    post = Post.query.get(UUID(post_id))

    if not post or post.is_delete:
        flash("Post not found", "error")
        return redirect(url_for("main.index"))

    postCreator = User.query.get(post.user_id)

    postDTO = PostDTO(post, postCreator, user)

    return render_template(
        "post/postDetail.html",
        post=postDTO.to_dict(),
        user=current_user,
        operation="read",
    )


@post.route("/new-post", methods=["GET"])
@login_required
@require_accept_community_guideline
def new_post():
    tags = Tag.query.all()
    tag_list = []
    for tag in tags:
        tag_list.append(
            {
                "id": tag.id,
                "name": tag.name,
                "color": tag.color,
            }
        )

    return render_template(
        "post/postDetail.html", user=current_user, tags=tag_list, operation="create"
    )


@post.route("/<post_id>/edit-post", methods=["GET"])
@login_required
@require_accept_community_guideline
def edit_post(post_id):
    post = Post.query.get(UUID(post_id))

    if not post or post.is_delete or post.status == PostStatus.PENDING:
        flash("Post not found", "error")
        return redirect(url_for("main.index"))

    tags = Tag.query.all()
    tag_list = []
    for tag in tags:
        tag_list.append({"id": tag.id, "name": tag.name, "color": tag.color})

    return render_template(
        "post/postDetail.html",
        user=current_user,
        tags=tag_list,
        operation="update",
        post=post,
    )
