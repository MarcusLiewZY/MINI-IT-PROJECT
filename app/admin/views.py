from flask import request, render_template, redirect, url_for
from flask_login import current_user

from . import admin
from app.models import Tag
from app.services.admin_service import get_agg_admin_notifications
from app.utils.decorators import (
    login_required,
    is_admin,
    require_accept_community_guideline,
)


@admin.route("/")
@login_required
@require_accept_community_guideline
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
