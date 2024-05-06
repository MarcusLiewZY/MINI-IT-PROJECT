
from uuid import UUID
from flask import flash, redirect, url_for, request, render_template
from datetime import datetime

from . import post

from flask_login import current_user

from app import db
from app.models.post import Post, Status
from app.models.tag import Tag
from app.models.user import User
from app.utils.helper import format_datetime

from app.utils.decorators import login_required


@post.route("/update-post/<post_id>", methods=["GET", "POST"])
@login_required
def update_post(post_id):
    post = Post.query.get(UUID(post_id))

    new_post = request.form

    if not post:
        flash("Post not found, please try again", "error")
        return redirect(url_for("main.index"))

    post.title = new_post.get("title")
    post.content = new_post.get("content")
    post.image_url = new_post.get("image_url")
    post.updated_at = format_datetime(datetime.now())

    for tag_name in new_post.getlist("tags"):
        tag = Tag.query.filter_by(name=tag_name).first()
        if not tag:
            flash("Tag not found, please try again", "error")
            return redirect(url_for("main.index"))

        post.tags.append(tag)

    db.session.commit()

    flash("Post updated successfully", "success")
    return redirect(url_for("main.index"))


@post.route("/delete-post/<post_id>", methods=["GET", "POST"])
@login_required
def delete_post(post_id):

    post = Post.query.get(UUID(post_id))

    if not post:
        flash("Post not found, please try again", "error")
        return redirect(url_for("main.index"))

    db.session.delete(post)
    db.session.commit()

    flash("Post deleted successfully", "success")
    return redirect(url_for("main.index"))


# get one post by id
@post.route("/posts/<post_id>")
@login_required
def get_post(post_id):
    tags = Tag.query.all()
    post = Post.query.get(UUID(post_id))

    if not post:
        flash("Post not found, please try again", "error")

    # find the author of the post
    author = User.query.get(post.user_id)

    post.author = author

    return render_template(
        "post/postDetail.html", post_stuff=post, tags=tags, isSinglePost=True
    )


# get all posts, create post
@post.route("/posts", methods=["GET", "POST"])
@login_required
def get_all_posts():
    if request.method == "POST":
        post_form = request.form
        new_post = Post(
            {
                "title": post_form.get("title"),
                "content": post_form.get("content"),
                "image_url": post_form.get("image_url"),
                "created_at": format_datetime(datetime.now()),
            }
        )

        new_post.user_id = current_user.id

        # todo: delete the approved status once the admin feature is implemented
        new_post.status = Status.APPROVED

        for tag_name in post_form.getlist("tags"):
            tag = Tag.query.filter_by(name=tag_name).first()
            if not tag:
                flash("Tag not found, please try again", "error")
                return redirect(url_for("main.index"))

            new_post.tags.append(tag)

        db.session.add(new_post)
        db.session.commit()

        flash("Post created successfully", "success")
        return redirect(url_for("main.index"))

    posts = Post.query.order_by(Post.updated_at.desc()).all()
    tags = Tag.query.all()

    return render_template(
        "post/postDetail.html", post_stuff=posts, tags=tags, isSinglePost=False
    )
