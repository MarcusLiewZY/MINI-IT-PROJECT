from flask_login import current_user
from flask import render_template, request, redirect, url_for

from . import notification
from app.services.notification_service import get_agg_notifications
from app.utils.decorators import login_required, require_accept_community_guideline


@notification.route("/notifications")
@login_required
@require_accept_community_guideline
def notifications():
    filter = request.args.get("filter")

    if filter is None:
        return redirect(url_for("notification.notifications", filter="all"))

    notificationsAgg = get_agg_notifications(current_user)

    notSourceHandlerMessages = {
        "messageTitles": [
            "No notifications yet!",
        ],
        "messageBodies": [
            "Check back later for new notifications.",
            "You're all caught up for now.",
        ],
    }

    return render_template(
        "notifications/notification.html",
        user=current_user,
        notificationsAgg=notificationsAgg,
        notSourceHandlerMessages=notSourceHandlerMessages,
    )
