from flask import render_template, redirect, url_for
from flask_login import current_user
from sqlalchemy import and_, desc

from . import me_bp
from app.models.post import Post, Status
from app.models.user import User
from app.dto.post_dto import PostDTO
from app.utils.decorators import login_required


@me_bp.route("/")
@login_required
def me():
    return redirect(url_for("me.posts"))


@me_bp.route("/posts")
@login_required
def posts():

    posts = (
        Post.query.filter(
            and_(Post.user_id == current_user.id, Post.status == Status.APPROVED)
        )
        .order_by(Post.updated_at.desc())
        .all()
    )

    postDTOs = [
        PostDTO(post, current_user, current_user, isPreview=True) for post in posts
    ]

    return render_template("me/posts.html", user=current_user, posts=postDTOs)


@me_bp.route("/likes")
@login_required
def likes():
    liked_posts = (
        User.query.filter(User.id == current_user.id)
        .join(User.liked_posts)
        .order_by(desc(Post.updated_at))
        .first()
        .liked_posts
    )

    postDTOs = [
        PostDTO(post, current_user, current_user, isPreview=True)
        for post in liked_posts
    ]

    print(postDTOs)

    return render_template("me/posts.html", user=current_user, posts=postDTOs)


@me_bp.route("/replies")
@login_required
def replies():

    posts = (
        Post.query.filter(
            and_(Post.user_id == current_user.id, Post.status == Status.APPROVED)
        )
        .order_by(Post.updated_at.desc())
        .all()
    )
    print(current_user.id)
    print(posts)

    postDTOs = [
        PostDTO(post, current_user, current_user, isPreview=True) for post in posts
    ]

    print(postDTOs)

    return render_template("me/posts.html", user=current_user, posts=postDTOs)


@me_bp.route("/bookmarks")
@login_required
def bookmarks():

    posts = (
        Post.query.filter(
            and_(Post.user_id == current_user.id, Post.status == Status.APPROVED)
        )
        .order_by(Post.updated_at.desc())
        .all()
    )
    print(current_user.id)
    print(posts)

    postDTOs = [
        PostDTO(post, current_user, current_user, isPreview=True) for post in posts
    ]

    print(postDTOs)

    return render_template("me/posts.html", user=current_user, posts=postDTOs)
