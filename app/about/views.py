from flask import render_template
from flask_login import current_user
from app.utils.decorators import login_required
from . import about_bp


@about_bp.route("/about")
@login_required
def get_about():
    return render_template("about/about.html", user=current_user)
