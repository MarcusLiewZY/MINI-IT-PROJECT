from flask_login import current_user
from flask import render_template, request

from . import notification
from app.services.notification_service import (
    get_all_notifications,
    get_post_notifications,
    get_comment_notifications,
    get_posts,
    get_agg_notifications,
)
from app.dto.notification_dto import NotificationDTO
from app.utils.decorators import login_required


@notification.route("/notifications")
@login_required
def notifications():
    filter = request.args.get("filter")
    notifications = []

    if filter == "posts":
        _, notifications = get_post_notifications(current_user)
    elif filter == "comments":
        _, notifications = get_comment_notifications(current_user)
    elif filter == "post-status":
        _, notifications = get_posts(current_user)
    else:
        _, notifications = get_all_notifications(current_user)

    notificationDTOs = [NotificationDTO(obj).to_dict() for obj in notifications]
    notificationsAgg = get_agg_notifications(current_user)

    # print(notificationDTOs)

    return render_template(
        "notifications/notification.html",
        user=current_user,
        notifications=notificationDTOs,
        notificationsAgg=notificationsAgg,
    )
