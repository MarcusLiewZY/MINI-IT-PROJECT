from datetime import datetime
from flask import render_template, request, flash, redirect, url_for
from flask_login import current_user, logout_user

from . import main
from app import db
from app.models import User
from app.utils.decorators import (
    login_required,
    logout_required,
    is_admin,
    require_accept_community_guideline,
    development_only,
)


@main.route("/", methods=["GET"])
@login_required
@require_accept_community_guideline
def index():
    user = User.query.get(current_user.id)

    return render_template(
        "main/index.html",
        user=user,
    )


@main.route("/results", methods=["GET"])
@login_required
@require_accept_community_guideline
def get_search_posts():

    notSourceHandlerMessages = {
        "messageTitles": [
            "OOPS! NO POSTS FOUND!",
        ],
        "messageBodies": [
            "We couldn't find any results for your search.",
            "Try adjusting your search or visit the homepage.",
        ],
    }

    return render_template(
        "post/searchPostResults.html",
        user=current_user,
        notSourceHandlerMessages=notSourceHandlerMessages,
    )


@main.route("/landing")
@logout_required
def landing():
    return render_template("main/landing.html")


@main.route("/community-guideline")
@login_required
def community_guidelines():

    if current_user.is_confirmed is False:
        logout_user()
        return redirect(url_for("main.landing"))

    user = User.query.get(current_user.id)
    need_confirm = True if user.anon_no is None else False
    return render_template(
        "main/communityGuidelines.html", need_confirm=need_confirm, user=user
    )


@main.route("/campus-selection", methods=["GET", "POST"])
@login_required
def campus_selection():

    # update the user anon number as the user accept the community guidelines
    if request.method == "POST":
        user = User.query.get(current_user.id)
        user.anon_no = User.generate_anon_no()
        db.session.commit()

    return render_template("campus-selection/campus.html", user=current_user)


@main.route("/campus-selection/<campus>")
@login_required
@require_accept_community_guideline
def campus_selection_handler(campus):
    user = User.query.get(current_user.id)
    user.campus = campus
    user.updated_at = datetime.now()
    db.session.commit()
    flash("Welcome to MMU Confession", "success")
    return redirect(url_for("main.index"))


@main.route("/playground")
@login_required
@is_admin
@development_only
def playground():
    # load a single file with multiple colors
    colors = [
        "red",
        "green",
        "blue",
        "black",
        "yellow",
        "purple",
        "orange",
        "pink",
        "brown",
        "gray",
    ]

    return render_template(
        "other/playground.html",
        user=current_user,
    )
