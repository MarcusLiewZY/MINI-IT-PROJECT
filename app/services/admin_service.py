from typing import List, Union, Tuple, Dict

from app.models import User, Post, Status, Comment
from app.dto import AdminNotificationDTO


def get_reporting_comments() -> Tuple[int, List[Comment]]:
    """
    Get all reporting comments order by updated-at in ascending order.
    Args:
        None
    Returns:
        Tuple[int, List[Comment]]: Number of reporting comments and reporting comments.
    """
    reporting_comments = (
        Comment.query.filter(Comment.is_report == True)
        .order_by(Comment.updated_at.asc())
        .all()
    )

    return len(reporting_comments), reporting_comments


def get_approving_post():
    """
    Get all pending posts order by updated at in ascending order.
    Args:
        None
    Returns:
        Tuple[int, List[Post]]: Number of approving posts and approving posts.
    """
    approving_post = (
        Post.query.filter(Post.status == Status.PENDING)
        .order_by(Post.updated_at.asc())
        .all()
    )

    return len(approving_post), approving_post


def get_all_admin_notifications() -> Tuple[int, List[Union[Post, Comment]]]:
    """
    Get all reporting comments and approving posts order by updated at in ascending order.
    """

    _, reporting_comments = get_reporting_comments()
    _, approving_posts = get_approving_post()

    all_admin_notifications = reporting_comments + approving_posts

    all_admin_notifications = sorted(
        all_admin_notifications, key=lambda x: x.updated_at, reverse=False
    )

    return len(all_admin_notifications), all_admin_notifications


def get_agg_admin_notifications():
    """
    Get the aggregated admin notifications, including the number of reporting comments, approving posts and all admin notifications.
    Args:
        None
    Returns:
        Dict[str, int]: Aggregated admin notifications.
    """

    reporting_comments_no, _ = get_reporting_comments()
    approving_posts_no, _ = get_approving_post()
    all_admin_notifications = reporting_comments_no + approving_posts_no

    return {
        "reportingComments": reporting_comments_no,
        "approvingPosts": approving_posts_no,
        "allAdminNotifications": all_admin_notifications,
    }


# pagination
def get_paginate_reporting_comments(
    page: int = 1, per_page: int = 10
) -> Tuple[bool, List[Comment]]:
    """
    Get all reporting comments order by updated_at in ascending order based on the pagination parameter (page).
    Args:
         page (int): The page number of the reporting comment list.
        per_page (int): The number of the reporting comments per page.
    Returns:
        Tuple[bool, List[Comment]]: A tuple containing a boolean indicating if there are more reporting comments and a list of adminNotificationDTOs.
    """

    reporting_comments = (
        Comment.query.filter(Comment.is_report == True)
        .order_by(Comment.updated_at.asc())
        .paginate(page=page, per_page=per_page, error_out=False)
    )

    has_next = reporting_comments.has_next
    reporting_comment_list = reporting_comments.items

    reportingCommentDTOs = [
        AdminNotificationDTO(obj).to_dict() for obj in reporting_comment_list
    ]

    return has_next, reportingCommentDTOs


def get_paginate_approving_post(
    page: int = 1, per_page: int = 10
) -> Tuple[bool, List[Post]]:
    """
    Get all approving posts order by updated_at in ascending order based on the pagination parameter (page).
    Args:
         page (int): The page number of the approving post list.
        per_page (int): The number of the approving posts per page.
    Returns:
        Tuple[bool, List[Comment]]: A tuple containing a boolean indicating if there are more approving posts and a list of adminNotificationDTOs.
    """

    # approving_posts = (
    #     Comment.query.filter(Comment.is_report == True)
    #     .order_by(Comment.updated_at.asc())
    #     .paginate(page=page, per_page=per_page, error_out=False)
    # )

    approving_posts = (
        Post.query.filter(Post.status == Status.PENDING)
        .order_by(Post.updated_at.asc())
        .paginate(page=page, per_page=per_page, error_out=False)
    )

    has_next = approving_posts.has_next
    approving_post_list = approving_posts.items

    approvingPostDTOs = [
        AdminNotificationDTO(obj).to_dict() for obj in approving_post_list
    ]

    return has_next, approvingPostDTOs


def get_paginate_all_admin_notifications(
    page: int = 1, per_page: int = 10
) -> Tuple[bool, List[Union[Post, Comment]]]:
    """
    Get all admin notifications order by updated_at in ascending order based on the pagination parameter (page).
    Args:
         page (int): The page number of the admin notification list.
        per_page (int): The number of the admin notifications per page.
    Returns:
        Tuple[bool, List[Union[Post, Comment]]]: A tuple containing a boolean indicating if there are more admin notifications and a list of adminNotificationDTOs.
    """
    _, reporting_comments = get_reporting_comments()
    _, approving_posts = get_approving_post()

    all_admin_notifications = reporting_comments + approving_posts

    all_admin_notifications = sorted(
        all_admin_notifications, key=lambda x: x.updated_at, reverse=False
    )

    start = (page - 1) * per_page
    end = start + per_page

    all_admin_notification_list = all_admin_notifications[start:end]
    has_next = end < len(all_admin_notifications)

    allAdminNotificationDTOs = [
        AdminNotificationDTO(obj).to_dict() for obj in all_admin_notification_list
    ]

    return has_next, allAdminNotificationDTOs
