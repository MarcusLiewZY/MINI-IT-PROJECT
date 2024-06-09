from flask import render_template, redirect, url_for, request, flash
from flask_login import current_user

from . import me_bp
from app import app, db
from app.services.me_service import get_user_agg_interaction
from app.utils.helper import upload_image, delete_image
from app.utils.decorators import login_required, require_accept_community_guideline

notSourceHandlerMessages = {
    "postsPage": {
        "messageTitles": [
            "No posts yet!",
        ],
        "messageBodies": [
            "Start sharing your thoughts with the world.",
        ],
    },
    "likesPage": {
        "messageTitles": [
            "No liked posts yet!",
        ],
        "messageBodies": [
            "Explore and like posts that you enjoy.",
        ],
    },
    "repliesPage": {
        "messageTitles": [
            "No replies yet!",
        ],
        "messageBodies": [
            "Join the conversation by replying to posts.",
        ],
    },
    "bookmarksPage": {
        "messageTitles": [
            "No bookmarks yet!",
        ],
        "messageBodies": [
            "Save posts that you find interesting to read later.",
        ],
    },
    "rejectedPostsPage": {
        "messageTitles": [
            "No rejected posts yet!",
        ],
        "messageBodies": [
            "All your posts are approved and visible.",
        ],
    },
}


@me_bp.route("/", methods=["GET", "POST"])
@login_required
@require_accept_community_guideline
def index():

    if request.method == "POST":
        avatar = request.files["avatar"]
        if not avatar:
            flash("No file is selected", "warning")
            return redirect(url_for("me.index"))

        avatar_url = upload_image(avatar, app.config["CLOUDINARY_AVATAR_IMAGE_FOLDER"])
        if not avatar_url:
            flash("Failed to upload the avatar", "warning")
            return redirect(url_for("me.index"))

        if current_user.avatar_url:
            is_deleted = delete_image(current_user.avatar_url)

            if not is_deleted:
                flash("Failed to upload the avatar", "warning")
                return redirect(url_for("me.index"))

        current_user.avatar_url = avatar_url
        db.session.commit()
        flash("Avatar updated successfully", "success")

    return redirect(url_for("me.posts"))


@me_bp.route("/posts", methods=["GET", "POST"])
@login_required
@require_accept_community_guideline
def posts():
    userAggInteraction = get_user_agg_interaction(current_user)

    return render_template(
        "me/posts.html",
        user=current_user,
        userAggInteraction=userAggInteraction,
        postContainerId="myPageCreatedPostCardContainer",
        notSourceHandlerMessages=notSourceHandlerMessages["postsPage"],
    )


@me_bp.route("/likes")
@login_required
@require_accept_community_guideline
def likes():
    userAggInteraction = get_user_agg_interaction(current_user)

    return render_template(
        "me/posts.html",
        user=current_user,
        userAggInteraction=userAggInteraction,
        postContainerId="myPageLikedPostCardContainer",
        notSourceHandlerMessages=notSourceHandlerMessages["likesPage"],
    )


@me_bp.route("/replies")
@login_required
@require_accept_community_guideline
def replies():

    userAggInteraction = get_user_agg_interaction(current_user)

    return render_template(
        "me/posts.html",
        user=current_user,
        userAggInteraction=userAggInteraction,
        postContainerId="myPageRepliesPostCardContainer",
        notSourceHandlerMessages=notSourceHandlerMessages["repliesPage"],
    )


@me_bp.route("/bookmarks")
@login_required
@require_accept_community_guideline
def bookmarks():

    userAggInteraction = get_user_agg_interaction(current_user)

    return render_template(
        "me/posts.html",
        user=current_user,
        userAggInteraction=userAggInteraction,
        postContainerId="myPageBookmarkedPostCardContainer",
        notSourceHandlerMessages=notSourceHandlerMessages["bookmarksPage"],
    )


@me_bp.route("/rejected-posts")
@login_required
@require_accept_community_guideline
def rejected_posts():

    userAggInteraction = get_user_agg_interaction(current_user)

    return render_template(
        "me/posts.html",
        user=current_user,
        userAggInteraction=userAggInteraction,
        postContainerId="myPageRejectedPostCardContainer",
        notSourceHandlerMessages=notSourceHandlerMessages["rejectedPostsPage"],
        isRejected=True,
    )
