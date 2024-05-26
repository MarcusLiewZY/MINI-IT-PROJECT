from typing import List, Dict, Union
from app.utils.helper import getTimeAgo
from app.models import User, Comment, CommentStatus


class CommentDTO:
    def __init__(self, comment: Comment, user: User, commentLevel: int):
        if not any([comment, user, commentLevel]):
            raise ValueError("comment and user are required")

        self.comment = comment
        self.commentLevel = commentLevel
        self.id = comment.id
        self.content = comment.content
        self.timeAgo = getTimeAgo(comment.updated_at)
        self.commentCreator = CommentDTO._get_user(comment.commentCreator)
        self.userInteraction = self._get_user_on_comment_interaction(comment)
        self.replies = None
        self.isReply = True if commentLevel > 1 and comment.replied_comment else False
        self.isLikedByUser = user in comment.liked_by
        self.isRepliedByUser = any(
            reply.commentCreator == user for reply in comment.replies
        )
        self.isReported = comment.status == CommentStatus.REPORTED

    @staticmethod
    def _get_user(user: User):
        return {
            "id": user.id,
            "user_name": user.username,
            "anon_no": user.anon_no,
            "avatar_url": user.avatar_url,
            "campus": user.campus.value,
            "is_admin": user.is_admin,
        }

    @staticmethod
    def _get_user_on_comment_interaction(comment: Comment) -> Dict[str, int]:
        return {"likes": len(comment.liked_by), "replies": len(comment.replies)}

    # @staticmethod
    def get_replies(self) -> List[Dict[str, Union[int, str, bool, List]]]:

        if not self.comment.replies:
            return []

        replies = []

        for reply in self.comment.replies:
            replyDTO = CommentDTO(reply, reply.commentCreator, self.commentLevel + 1)

            replyDTO.get_replies()

            replies.append(replyDTO.to_dict())

        self.replies = replies

    def to_dict(self):
        return {
            "commentLevel": self.commentLevel,
            "id": self.id,
            "content": self.content,
            "timeAgo": self.timeAgo,
            "commentCreator": self.commentCreator,
            "userInteraction": self.userInteraction,
            "replies": self.replies,
            "isReply": self.isReply,
            "isLikedByUser": self.isLikedByUser,
            "isRepliedByUser": self.isRepliedByUser,
            "isReported": self.isReported,
        }
