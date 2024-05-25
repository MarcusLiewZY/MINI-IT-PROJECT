from typing import List, Union, Tuple, Dict

from app.models import PostNotification, CommentNotification, Post, User, PostStatus
from app.dto.notification_dto import NotificationDTO


# utility function
def custom_sort(obj):
    """
    Custom sort function to sort the object by created_at or updated_at. For the post, sort it by updated_at, while for the comment and post notification, sort it by created_at.
    Args:
        obj: The object which needs to be sorted.
    Returns:
        The created_at or updated_at attribute of the object.
    """
    if isinstance(obj, Post):
        return obj.updated_at
    else:
        return obj.created_at


def get_post_notifications(user: User) -> Tuple[int, List[PostNotification]]:
    """
    Get all post notifications order by created_at in ascending order.
    Args:
        user (User): The user who is logged in. The user who is be notified.
    Returns:
        The number of post notifications and the list of post notifications.
    """
    post_notifications = (
        PostNotification.query.filter(
            PostNotification.user_id == user.id, PostNotification.is_read == False
        )
        .order_by(PostNotification.created_at.asc())
        .all()
    )
    return len(post_notifications), post_notifications


def get_comment_notifications(user: User) -> Tuple[int, List[CommentNotification]]:
    """
    Get all comment notifications order by created_at in ascending order.
    Args:
        user (User): The user who is logged in. The user who is be notified.
    Returns:
        The number of comment notifications and the list of comment notifications.
    """
    comment_notifications = (
        CommentNotification.query.filter(
            CommentNotification.user_id == user.id, CommentNotification.is_read == False
        )
        .order_by(CommentNotification.created_at.asc())
        .all()
    )

    return len(comment_notifications), comment_notifications


def get_posts(user: User) -> Tuple[int, List[Post]]:
    """
    Get all posts with the conditions:
    case 1: the post creator is the user, post status is pending
    case 2: the post creator is the user, and the post status is either unread-approved or unread-rejected, and the created_at is different from updated_at. This is because when the admin approve or reject the post, the updated_at will be updated. When the click the rejected and approved post, the updated_at will be updated again.
    Args:
        user (User): The user who is logged in. The user who is be notified.
    Returns:
        The number of posts and the list of posts.
    """
    posts = (
        Post.query.filter(
            (Post.user_id == user.id)
            & (
                (Post.status == PostStatus.PENDING)
                | (
                    (
                        Post.status.in_(
                            [PostStatus.UNREAD_APPROVED, PostStatus.UNREAD_REJECTED]
                        )
                    )
                    & (Post.created_at != Post.updated_at)
                )
            )
        )
        .order_by(Post.updated_at.asc())
        .all()
    )

    return len(posts), posts


def get_all_notifications(
    user: User,
) -> Tuple[int, List[Union[PostNotification, CommentNotification, Post]]]:
    """
    Get all notifications including the post notifications, comment notifications and the post status order by created_at in ascending order.
    Args:
        user (User): The user who is logged in. The user who is be notified.
    Returns:

    """
    _, post_notifications = get_post_notifications(user)
    _, comment_notifications = get_comment_notifications(user)
    _, posts = get_posts(user)

    # combine the all notifications
    all_notifications = post_notifications + comment_notifications + posts

    # for the post and comment notifications, sort it by created_at in ascending order, while for the post, sort it by updated_at in ascending order.
    all_notifications = sorted(all_notifications, key=custom_sort, reverse=False)

    return len(all_notifications), all_notifications


def get_agg_notifications(user) -> Dict[str, int]:
    """
    Get the aggregated notifications for the user, including the number of post notifications, comment notifications, posts and all notifications.
    Args:
        user (User): The user who is logged in. The user who is be notified.
    Returns:
        The aggregated notifications for the user.
    """

    post_notifications_no, _ = get_post_notifications(user)
    comment_notifications_no, _ = get_comment_notifications(user)
    posts_no, _ = get_posts(user)
    all_notifications = post_notifications_no + comment_notifications_no + posts_no

    return {
        "postNotifications": post_notifications_no,
        "commentNotifications": comment_notifications_no,
        "posts": posts_no,
        "allNotifications": all_notifications,
    }


# pagination
def get_paginate_post_notifications(
    user: User, page: int = 1, per_page: int = 10
) -> Tuple[bool, List[PostNotification]]:
    """
    Get all post notifications order by created_at in ascending order based on the pagination parameter (page).
    Args:
        user (User): The user who is logged in. The user who is be notified.
         page (int): The page number of the post notification list.
        per_page (int): The number of the post notifications per page.
    Returns:
        Tuple[bool, List[PostNotification]]: A tuple containing a boolean indicating if there are more post notifications and a list of notificationDTOs.
    """
    post_notifications = (
        PostNotification.query.filter(
            PostNotification.user_id == user.id, PostNotification.is_read == False
        )
        .order_by(PostNotification.created_at.asc())
        .paginate(page=page, per_page=per_page, error_out=False)
    )

    has_next = post_notifications.has_next
    post_notification_list = post_notifications.items

    postNotificationDTOs = [
        NotificationDTO(obj).to_dict() for obj in post_notification_list
    ]

    return has_next, postNotificationDTOs


def get_paginate_comment_notifications(
    user: User, page: int = 1, per_page: int = 10
) -> Tuple[bool, List[CommentNotification]]:
    """
    Get all comment notifications order by created_at in ascending order based on the pagination parameter (page and per_page).
    Args:
        user (User): The user who is logged in. The user who is be notified.
        page (int): The page number of the post list.
        per_page (int): The number of the posts per page.
    Returns:
        Tuple[bool, List[PostNotification]]: A tuple containing a boolean indicating if there are more comment notifications and a list of notificationDTOs.
    """
    comment_notifications = (
        CommentNotification.query.filter(
            CommentNotification.user_id == user.id, CommentNotification.is_read == False
        )
        .order_by(CommentNotification.created_at.asc())
        .paginate(page=page, per_page=per_page, error_out=False)
    )

    has_next = comment_notifications.has_next
    comment_notification_list = comment_notifications.items

    commentNotificationDTOs = [
        NotificationDTO(obj).to_dict() for obj in comment_notification_list
    ]

    return has_next, commentNotificationDTOs


def get_paginate_posts(
    user: User, page: int = 1, per_page: int = 10
) -> Tuple[bool, List[Post]]:
    """
    Get all posts with the conditions:
    case 1: the post creator is the user, post status is pending
    case 2: the post creator is the user, and the post status is either unread-approved or unread-rejected, and the created_at is different from updated_at. This is because when the admin approve or reject the post, the updated_at will be updated. When the click the rejected and approved post, the updated_at will be updated again.
    This is based on the pagination parameter (page and per_page).
    Args:
        user (User): The user who is logged in. The user who is be notified.
        page (int): The page number of the post list.
        per_page (int): The number of the posts per page.
    Returns:
         Tuple[bool, List[PostNotification]]: A tuple containing a boolean indicating if there are more notified posts and a list of notificationDTOs.
    """
    posts = (
        Post.query.filter(
            (Post.user_id == user.id)
            & (
                (Post.status == PostStatus.PENDING)
                | (
                    (
                        Post.status.in_(
                            [PostStatus.UNREAD_APPROVED, PostStatus.UNREAD_REJECTED]
                        )
                    )
                    & (Post.created_at != Post.updated_at)
                )
            )
        )
        .order_by(Post.updated_at.asc())
        .paginate(page=page, per_page=per_page, error_out=False)
    )

    has_next = posts.has_next
    post_list = posts.items

    postDTOs = [NotificationDTO(obj).to_dict() for obj in post_list]

    return has_next, postDTOs


def get_paginate_all_notifications(
    user: User, page: int = 1, per_page: int = 10
) -> Tuple[bool, List[Union[PostNotification, CommentNotification, Post]]]:
    """
    Get all notifications including the post notifications, comment notifications and the post status order by created_at in ascending order based on the pagination parameter (page and per_page).
    Args:
        user (User): The user who is logged in. The user who is be notified.
    Returns:

    """
    _, post_notifications = get_post_notifications(user)
    _, comment_notifications = get_comment_notifications(user)
    _, posts = get_posts(user)

    # combine the all notifications
    all_notifications = post_notifications + comment_notifications + posts

    # for the post and comment notifications, sort it by created_at in ascending order, while for the post, sort it by updated_at in ascending order.
    all_notifications = sorted(all_notifications, key=custom_sort, reverse=False)

    start = (page - 1) * per_page
    end = start + per_page

    all_notification_list = all_notifications[start:end]
    has_next = end < len(all_notifications)

    allNotificationDTOs = [
        NotificationDTO(obj).to_dict() for obj in all_notification_list
    ]

    return has_next, allNotificationDTOs
