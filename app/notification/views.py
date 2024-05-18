from flask_login import current_user
from flask import render_template, request, redirect, url_for

from . import notification
from app.services.notification_service import get_agg_notifications
from app.dto.notification_dto import NotificationDTO
from app.utils.decorators import login_required


@notification.route("/notifications")
@login_required
def notifications():
    filter = request.args.get("filter")

    if filter is None:
        return redirect(url_for("notification.notifications", filter="all"))

    notificationsAgg = get_agg_notifications(current_user)

    return render_template(
        "notifications/notification.html",
        user=current_user,
        notificationsAgg=notificationsAgg,
    )
