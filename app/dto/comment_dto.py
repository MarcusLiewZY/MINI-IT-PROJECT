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
    def get_replies(
        self, maxCommentLevel: int, isPreview: bool
    ) -> List[Dict[str, Union[int, str, bool, List]]]:
        # base case: no replies or max comment level reached
        if not self.comment.replies or self.commentLevel >= maxCommentLevel:
            return []

        # base case for preview version
        if isPreview and self.commentLevel >= 2:
            return []

        replyDTOs = []

        # order by updated_at
        replies = sorted(
            self.comment.replies, key=lambda reply: reply.created_at, reverse=False
        )

        for reply in replies:

            # stop the loop if the post is a preview and the number of the comments is 3
            if isPreview and len(replyDTOs) >= 3:
                break

            elif reply:
                # if the comment is a reply on the first comment level, skip it
                if self.commentLevel == 1 and self.comment.replied_comment:
                    continue

                replyDTO = CommentDTO(
                    reply, reply.commentCreator, self.commentLevel + 1
                )

                replyDTO.get_replies(
                    maxCommentLevel=maxCommentLevel,
                    isPreview=isPreview,
                )

                replyDTOs.append(replyDTO.to_dict())

        self.replies = replyDTOs

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
