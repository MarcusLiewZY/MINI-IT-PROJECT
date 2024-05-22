from flask import request, render_template, flash, redirect, url_for
from flask_login import login_user, current_user

from . import admin
from app.models import User, Tag
from app.utils.decorators import logout_required, login_required, is_admin
from app.services.admin_service import get_agg_admin_notifications


@admin.route("")
@login_required
@is_admin
def index():
    filter = request.args.get("filter")

    tags = Tag.query.all()

    if filter is None:
        return redirect(url_for("admin.index", filter="all"))

    adminNotificationsAgg = get_agg_admin_notifications()

    return render_template(
        "admin/admin.html",
        user=current_user,
        adminNotificationsAgg=adminNotificationsAgg,
        tags=tags,
    )


@admin.route("/sign-up", methods=["GET", "POST"])
@logout_required
def admin_login():
    if request.method == "POST":
        email = request.form.get("email")
        user = User.query.filter_by(email=email).first()

        if user and user.is_admin:
            login_user(user)
            flash("Successfully logged in", "success")
            return redirect(url_for("admin.index"))
        else:
            flash("You are not an admin user", "warning")
            return redirect(url_for("main.landing"))

    return render_template("main/adminLogin.html")
