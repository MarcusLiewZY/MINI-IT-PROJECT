from flask import request, render_template, flash, redirect, url_for
from flask_login import login_user, current_user

from . import admin
from app.utils.decorators import logout_required, login_required, is_admin
from app.utils.helper import format_datetime
from app.models import User

@admin.route("/")
@login_required
@is_admin
def index():
    user = User.query.get(current_user.id)
    user.create_at = format_datetime(user.created_at)
    return render_template("main/admin.html", user=user)


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
