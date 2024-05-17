from app.models import Post, Comment, PostNotification, CommentNotification
from app import db
from app.utils.helper import getTimeAgo


class NotificationDTO:
    def __init__(self, obj):
        self.obj = obj

    def get_type(self, obj):
        if isinstance(obj, PostNotification):
            return "PostNotification"
        elif isinstance(obj, CommentNotification):
            return "CommentNotification"
        elif isinstance(obj, Post):
            return "Post"
        else:
            return None

    def construct_post_notification(self, post_notification: PostNotification):
        if post_notification is None:
            return None

        post = Post.query.filter(Post.id == post_notification.post_id).first()
        comment = Comment.query.filter(
            Comment.id == post_notification.unread_comment_id
        ).first()

        if post is None or comment is None:
            return None

        return {
            "type": self.get_type(post_notification),
            "postId": post.id,
            "postTitle": post.title,
            "postTags": [(tag.name, tag.color) for tag in post.tags],
            "commentCreator": comment.commentCreator,
            "commentContent": comment.content,
            "timeAgo": getTimeAgo(post_notification.created_at),
        }

    def construct_comment_notification(self, comment_notification: CommentNotification):
        if comment_notification is None:
            return None

        reply = Comment.query.filter(
            Comment.id == comment_notification.unread_comment_id
        ).first()

        if reply is None:
            return None

        replied_comment_creator = reply.replied_comment.commentCreator

        return {
            "type": self.get_type(comment_notification),
            "replyId": reply.id,
            "replyCommentCreator": reply.commentCreator,
            "replyContent": reply.content,
            "repliedToUser": replied_comment_creator,
            "timeAgo": getTimeAgo(comment_notification.created_at),
        }

    def construct_post(self, post: Post):
        if post is None:
            return None

        return {
            "type": self.get_type(post),
            "postId": post.id,
            "postTitle": post.title,
            "postTags": [(tag.name, tag.color) for tag in post.tags],
            "postStatus": post.status.value,
            "postContent": post.content,
            "postImageUrl": post.image_url if post.image_url else None,
            "timeAgo": getTimeAgo(post.updated_at),
        }

    def to_dict(self):
        if isinstance(self.obj, PostNotification):
            return self.construct_post_notification(self.obj)
        elif isinstance(self.obj, CommentNotification):
            return self.construct_comment_notification(self.obj)
        elif isinstance(self.obj, Post):
            return self.construct_post(self.obj)
        else:
            return None
