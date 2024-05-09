from typing import List, Dict, Union

from app.models import Post, Status, User
from app.dto.post_dto import PostDTO


def get_posts(
    user: User, isPreview: bool = False
) -> List[Dict[str, Union[str, int, bool, List]]]:
    """
    Get all posts ordered by updated_at in descending order by default.
    Args:
        user (User): The user who is currently logged in.
        isPreview (bool): A flag to determine if the post is a preview.
    Returns:
        List[Dict[str, Union[str, int, bool, List]]]: A list of post data transfer objects.
    """
    posts = (
        Post.query.filter_by(status=Status.APPROVED)
        .order_by(Post.updated_at.desc())
        .all()
    )

    print(posts[1].postCreator)

    postDTOs = [
        PostDTO(post, post.postCreator, user, isPreview).to_dict() for post in posts
    ]

    return postDTOs
