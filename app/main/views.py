import os
from flask import render_template, request, flash, redirect, url_for
from flask_login import current_user
from app.utils.decorators import login_required, logout_required
from datetime import datetime

from . import main
from app import db
from app.models import User, Campus, Tag
from app.forms import CreatePostForm
from app.services.post_service import get_posts, create_post


@main.route("/", methods=["GET"])
@login_required
def index():
    # createPostForm = CreatePostForm()
    # createPostForm.set_tag_choices()
    # if createPostForm.validate_on_submit():
    #     isSuccess, message = create_post(createPostForm)
    #     flash(message, "success" if isSuccess else "error")
    #     if isSuccess:
    #         return redirect(url_for("main.index"))

    user = User.query.get(current_user.id)
    # tags = Tag.query.all()

    return render_template(
        "main/index.html",
        user=user,
        # tags=tags,
        # createPostForm=createPostForm,
    )


@main.route("/landing")
@logout_required
def landing():
    return render_template("main/landing.html")


@main.route("/community-guideline")
@login_required
def community_guidelines():
    user = User.query.get(current_user.id)
    need_confirm = True if user.campus is Campus.NONE else False
    return render_template(
        "main/communityGuidelines.html", need_confirm=need_confirm, user=user
    )


@main.route("/campus-selection", methods=["GET", "POST"])
@login_required
def campus_selection():
    return render_template("campus-selection/campus.html", user=current_user)


@main.route("/campus-selection/<campus>")
def campus_selection_handler(campus):
    user = User.query.get(current_user.id)
    user.campus = campus
    user.updated_at = datetime.now()
    db.session.commit()
    flash("Welcome to MMU Confession", "success")
    return redirect(url_for("main.index"))


@main.route("/playground")
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

    admin_svg_list = []

    svg_path = "app/static/svg/Cross.svg"

    with open(svg_path, "r") as svg_file:
        svg_content = svg_file.read()

    for color in colors:
        svg = svg_content.replace('fill="black"', f'fill="{color}"')
        admin_svg_list.append(svg)

    # load multiple file from a same directory
    svg_dir = "app/static/svg"
    svg_files = []

    for file_name in os.listdir(svg_dir):
        if file_name.endswith(".svg"):
            svg_path = os.path.join(svg_dir, file_name)

            with open(svg_path, "r") as svg_file:
                svg_content = svg_file.read()

            svg_files.append(svg_content)

    hello, postDTOs = get_posts(current_user, isPreview=False, page=1, per_page=3)

    return render_template(
        "other/playground.html",
        admin_svg_list=admin_svg_list,
        svg_files=svg_files,
        posts=postDTOs,
        user=current_user,
    )
