from flask import render_template, redirect, url_for, request, flash
from flask_login import current_user

from . import me_bp
from app.utils.decorators import login_required
from app.services.me_service import get_user_agg_interaction
from app.utils.helper import upload_image, delete_image
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

        if current_user.avatar_url:
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
    userAggInteraction = get_user_agg_interaction(current_user)

    return render_template(
        "me/posts.html",
        user=current_user,
        userAggInteraction=userAggInteraction,
        postContainerId="myPageCreatedPostCardContainer",
    )


@me_bp.route("/likes")
@login_required
def likes():
    userAggInteraction = get_user_agg_interaction(current_user)

    return render_template(
        "me/posts.html",
        user=current_user,
        userAggInteraction=userAggInteraction,
        postContainerId="myPageLikedPostCardContainer",
    )


@me_bp.route("/replies")
@login_required
def replies():

    # the user's comments to the posts that is not reported, and the replies to the comments
    # return the posts that the user commented on and the replies to the comments

    userAggInteraction = get_user_agg_interaction(current_user)

    return render_template(
        "me/posts.html",
        user=current_user,
        userAggInteraction=userAggInteraction,
        postContainerId="myPageRepliesPostCardContainer",
    )


@me_bp.route("/bookmarks")
@login_required
def bookmarks():

    userAggInteraction = get_user_agg_interaction(current_user)

    return render_template(
        "me/posts.html",
        user=current_user,
        userAggInteraction=userAggInteraction,
        postContainerId="myPageBookmarkedPostCardContainer",
    )


@me_bp.route("/rejected-posts")
@login_required
def rejected_posts():

    userAggInteraction = get_user_agg_interaction(current_user)

    return render_template(
        "me/posts.html",
        user=current_user,
        userAggInteraction=userAggInteraction,
        postContainerId="myPageRejectedPostCardContainer",
        isRejected=True,
    )
