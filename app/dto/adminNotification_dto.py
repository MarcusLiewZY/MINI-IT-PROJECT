from app.models import Post, Comment
from app import db
from app.utils.helper import getTimeAgo


class AdminNotificationDTO:
    def __init__(self, obj):
        self.obj = obj

    def get_type(self, obj):
        if isinstance(obj, Comment):
            return "ReportingComment"
        elif isinstance(obj, Post):
            return "ApprovingPost"
        else:
            return None

    def construct_reporting_comment(self, reporting_comment: Comment):
        if reporting_comment is None:
            return None

        reporting_comment = Comment.query.filter(
            Comment.id == reporting_comment.id
        ).first()

        if reporting_comment is None:
            return None

        replied_comment_creator = None

        if reporting_comment.replied_comment:
            replied_comment_creator = reporting_comment.replied_comment.commentCreator

        return {
            "type": self.get_type(reporting_comment),
            "id": reporting_comment.id,
            "isReply": True if reporting_comment.replied_comment else False,
            "commentCreator": reporting_comment.commentCreator,
            "commentContent": reporting_comment.content,
            "repliedToUser": replied_comment_creator,
            "timeAgo": getTimeAgo(reporting_comment.created_at),
        }

    def construct_approving_post(self, approving_post: Post):
        if approving_post is None:
            return None

        return {
            "type": self.get_type(approving_post),
            "id": approving_post.id,
            "postTitle": approving_post.title,
            "postTags": [(tag.name, tag.color) for tag in approving_post.tags],
            "postStatus": approving_post.status,
            "postContent": approving_post.content,
            "postImageUrl": (
                approving_post.image_url if approving_post.image_url else None
            ),
            "timeAgo": getTimeAgo(approving_post.updated_at),
        }

    def to_dict(self):
        if isinstance(self.obj, Comment):
            return self.construct_reporting_comment(self.obj)
        elif isinstance(self.obj, Post):
            return self.construct_approving_post(self.obj)
        else:
            return None
