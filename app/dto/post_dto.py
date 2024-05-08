from app.utils.helper import getTimeAgo


# isPreview
# a post with maximum 3 comments, and each comment with maximum 3 replies
# maximum comment level is 2


class PostDTO:
    def __init__(self, post, postCreator, user, isPreview=False):
        if not any([post, postCreator, user]):
            raise ValueError("post, postCreator and user are required")

        self.id = post.id if post else None
        self.title = post.title if post else None
        self.content = post.content if post else None
        self.image_url = post.image_url if post else None
        self.tags = [(tag.name, tag.color) for tag in post.tags] or []
        self.timeAgo = getTimeAgo(post.updated_at) if post else None
        self.postCreator = self.get_user(postCreator)
        self.isCreator = True if postCreator.id == user.id else False
        self.isPreview = isPreview
        self.userInteraction = self.get_user_on_post_interaction(post, user)
        self.comments = self.get_comments(post.comments, level=1)

    def __repr__(self) -> str:
        return f"<PostDTO {self.title}>"

    def get_user(self, user):
        return {
            "id": user.id,
            "username": user.username,
            "anon_no": user.anon_no,
            "avatar_url": user.avatar_url,
            "campus": user.campus.value,
            "is_admin": user.is_admin,
        }

    def get_user_on_post_interaction(self, post, user):
        return {
            "likes": len(post.liked_by),
            "comments": len(post.comments),
            "isLikedByUser": user in post.liked_by,
            "isBookmarkedByUser": user in post.bookmarked_by,
        }

    def get_comments(self, comments, level):
        # base case
        if not comments:
            return []

        newComments = []

        for comment in comments:
            # stop the loop if the post is a preview and the number of comments is 3
            if self.isPreview and len(newComments) >= 3:
                break
            elif comment and not comment.is_report:
                if level == 1 and comment.replied_comment:
                    level = -1
                newComments.append(
                    {
                        "commentLevel": level,
                        "id": comment.id,
                        "content": comment.content,
                        "timeAgo": getTimeAgo(comment.updated_at),
                        "commentCreator": self.get_user(comment.commentCreator),
                        "userInteraction": self.get_user_on_comment_interaction(
                            comment
                        ),
                        "replies": self.get_comments(comment.replies, level + 1),
                        "isReply": True if comment.replied_comment else False,
                    }
                )

        return newComments

    def get_user_on_comment_interaction(self, comment):
        return {"likes": len(comment.liked_by), "replies": len(comment.replies)}

    def to_dict(self):
        return {
            "id": self.id,
            "title": self.title,
            "content": self.content,
            "image_url": self.image_url,
            "tags": self.tags,
            "timeAgo": self.timeAgo,
            "postCreator": self.postCreator,
            "isCreator": self.isCreator,
            "isPreview": self.isPreview,
            "userInteraction": self.userInteraction,
            "comments": self.comments,
        }
