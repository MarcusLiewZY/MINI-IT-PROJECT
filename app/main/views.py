from flask import render_template
from flask_login import current_user
from app.utils.decorators import login_required, logout_required

from . import main
from app.models.user import User
from app.utils.helper import format_datetime


@main.route("/")
@login_required
def index():
    user = User.query.get(current_user.id)
    user.created_at = format_datetime(user.created_at)
    return render_template("main/index.html", user=user)


@main.route("/landing")
@logout_required
def landing():
    return render_template("main/landing.html")
