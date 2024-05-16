from flask import render_template, redirect, url_for, request, flash
from flask_login import current_user
from sqlalchemy import and_, desc

from . import me_bp
from app.models import Post, Status, User, PostLike, PostBookmark, Comment
from app.dto.post_dto import PostDTO
from app.utils.decorators import login_required
from app.services.me_service import get_user_agg_interaction
from app.utils.helper import upload_image, delete_image, parse_datetime
from app import app, db


@me_bp.route("/", methods=["GET", "POST"])
@login_required
def index():

    if request.method == "POST":
        avatar = request.files["avatar"]
        if not avatar:
            flash("No file is selected", "danger")
            return redirect(url_for("me.index"))

        avatar_url = upload_image(avatar, app.config["CLOUDINARY_AVATAR_IMAGE_FOLDER"])
        if not avatar_url:
            flash("Failed to upload the avatar", "danger")
            return redirect(url_for("me.index"))

        is_deleted = delete_image(current_user.avatar_url)

        if not is_deleted:
            flash("Failed to upload the avatar", "danger")
            return redirect(url_for("me.index"))

        current_user.avatar_url = avatar_url
        db.session.commit()
        flash("Avatar updated successfully", "success")

    return redirect(url_for("me.posts"))


@me_bp.route("/posts", methods=["GET", "POST"])
@login_required
def posts():
    if request.method == "POST":
        print("POST")

    posts = (
        Post.query.filter(
            Post.user_id == current_user.id,
            Post.status == Status.APPROVED,
            Post.is_delete == False,
        )
        .order_by(Post.updated_at.desc())
        .all()
    )

    postDTOs = [
        PostDTO(post, post.postCreator, current_user, isPreview=True).to_dict()
        for post in posts
    ]

    posts = {
        "userAggInteraction": get_user_agg_interaction(current_user),
        "postList": postDTOs,
    }

    return render_template("me/posts.html", user=current_user, posts=posts)


@me_bp.route("/likes")
@login_required
def likes():
    liked_posts = (
        Post.query.filter(
            Post.user_id == current_user.id,
            Post.status == Status.APPROVED,
            Post.is_delete == False,
        )
        .join(PostLike, PostLike.c.post_id == Post.id)
        .filter(PostLike.c.user_id == current_user.id)
        .order_by(desc(PostLike.c.created_at))
        .all()
    )

    postDTOs = [
        PostDTO(post, post.postCreator, current_user, isPreview=True)
        for post in liked_posts
    ]

    posts = {
        "userAggInteraction": get_user_agg_interaction(current_user),
        "postList": postDTOs,
    }

    return render_template("me/posts.html", user=current_user, posts=posts)


@me_bp.route("/replies")
@login_required
def replies():

    # the user's comments to the posts that is not reported, and the replies to the comments
    # return the posts that the user commented on and the replies to the comments

    all_commented_posts = set()

    for comment in current_user.comments:
        if (
            comment.commented_post.status == Status.APPROVED
            and not comment.commented_post.is_delete
        ):
            all_commented_posts.add(comment.commented_post)

    postDTOs = [
        PostDTO(
            commented_post,
            commented_post.postCreator,
            current_user,
            isPreview=True,
        )
        for commented_post in all_commented_posts
    ]

    posts = {
        "userAggInteraction": get_user_agg_interaction(current_user),
        "postList": postDTOs,
    }

    return render_template("me/posts.html", user=current_user, posts=posts)


@me_bp.route("/bookmarks")
@login_required
def bookmarks():

    # bookmarked_posts = (
    #     User.query.filter(User.id == current_user.id)
    #     .join(PostBookmark, PostBookmark.c.user_id == User.id)
    #     .join(Post, Post.id == PostBookmark.c.post_id)
    #     .order_by(desc(PostBookmark.c.created_at))
    #     .first()
    #     .bookmarked_posts
    # )

    bookmarked_posts = (
        Post.query.filter(
            Post.user_id == current_user.id,
            Post.status == Status.APPROVED,
            Post.is_delete == False,
        )
        .join(PostBookmark, Post.id == PostBookmark.c.post_id)
        .filter(PostBookmark.c.user_id == current_user.id)
        .order_by(desc(PostBookmark.c.created_at))
        .all()
    )

    postDTOs = [
        PostDTO(post, post.postCreator, current_user, isPreview=True).to_dict()
        for post in bookmarked_posts
    ]

    posts = {
        "userAggInteraction": get_user_agg_interaction(current_user),
        "postList": postDTOs,
    }

    return render_template("me/posts.html", user=current_user, posts=posts)
