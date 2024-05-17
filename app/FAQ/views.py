from flask import render_template
from flask_login import current_user
from app.utils.decorators import login_required
from . import faq


@faq.route("/FAQ")
@login_required
def FAQ():
    return render_template("FAQ/FAQ.html", user=current_user)
