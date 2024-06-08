from datetime import datetime, timedelta, timezone
from typing import List, Tuple, Dict, Union
from sqlalchemy import func, and_, or_, text

from app import db
from app.models import Post, PostStatus, Tag, User
from app.dto.post_dto import PostDTO


class PostSearchEngine:
    def __init__(self):
        pass

    def _get_search_pattern(self, search_text):
        return f"%{search_text}%"

    def _get_ts_query(self, search_text):
        """
        Get ts_query for full text search.
        """

        return func.plainto_tsquery(search_text)

    def _get_rank_title(self, search_text):
        """
        Get the rank of the relevance of the title to the post.
        """
        return func.ts_rank_cd(
            func.to_tsvector("english", Post.title), self._get_ts_query(search_text)
        ).label("rank_title")

    def _get_rank_content(self, search_text):
        """
        Get the rank of the relevance of the content to the post.
        """
        return func.ts_rank_cd(
            func.to_tsvector("english", Post.content), self._get_ts_query(search_text)
        ).label("rank_content")

    def _get_updated_time_filter(self, updated_time_filter):
        """
        Get the filter for post updated time.
        """
        now = datetime.now(timezone.utc)

        updated_time_filters = {
            "Last hour": now - timedelta(hours=1),
            "Today": now - timedelta(days=1),
            "This week": now - timedelta(days=7),
            "This month": now - timedelta(days=30),
            "This year": now - timedelta(days=365),
        }

        return updated_time_filters.get(updated_time_filter, None)

    def _get_type_filters(self, type_filter, search_text, search_pattern):
        """
        Get the filter for post type.
        It can be applied to both title and content, only title, or only content.
        It use full text search and ilike for the filter.
        """

        type_filters = {
            "all": or_(
                func.to_tsvector("english", Post.title).match(search_text),
                Post.title.ilike(search_pattern),
                func.to_tsvector("english", Post.content).match(search_text),
                Post.content.ilike(search_pattern),
            ),
            "post title": or_(
                func.to_tsvector("english", Post.title).match(search_text),
                Post.title.ilike(search_pattern),
            ),
            "post content": or_(
                func.to_tsvector("english", Post.content).match(search_text),
                Post.content.ilike(search_pattern),
            ),
        }
        return type_filters.get(type_filter, None)

    def _get_sorting_options(self, sort_by):
        """
        Get the sorting options for the search result.
        """
        sorting_options = {
            "relevance": text("rank_title DESC, rank_content DESC"),
            "latest": Post.updated_at.desc(),
            "oldest": Post.updated_at.asc(),
        }
        return sorting_options.get(sort_by, None)

    def _filter_by_tags(self, query, tag_filter):
        """
        Filter the posts by tags.
        """
        if tag_filter and "None" not in tag_filter:
            query = query.join(Post.tags).filter(Tag.name.in_(tag_filter))
        return query

    def _construct_search_query(self, page, per_page, search_dist):
        """
        Search posts by search_text, updated_time_filter, type_filter, tag_filter, and sort_by.
        """

        search_text = search_dist.get("search_text", None)
        updated_time_filter = search_dist.get("updated_time_filter", None)
        type_filter = search_dist.get("type_filter", None)
        tag_filter = search_dist.get("tag_filter", None)
        sort_by = search_dist.get("sort_by", None)

        search_pattern = self._get_search_pattern(search_text)
        rank_title = self._get_rank_title(search_text)
        rank_content = self._get_rank_content(search_text)

        query = db.session.query(Post, rank_title, rank_content).filter(
            and_(
                Post.status.in_([PostStatus.APPROVED, PostStatus.UNREAD_APPROVED]),
                Post.is_delete == False,
            )
        )

        updated_time_filter = self._get_updated_time_filter(updated_time_filter)
        if updated_time_filter:
            query = query.filter(Post.updated_time >= updated_time_filter)

        type_filters = self._get_type_filters(type_filter, search_text, search_pattern)
        if type_filters is not None:
            query = query.filter(type_filters)

        query = self._filter_by_tags(query, tag_filter)

        sorting_options = self._get_sorting_options(sort_by)

        if sorting_options is not None:
            query = query.order_by(sorting_options)

        results = query.paginate(page=page, per_page=per_page, error_out=False)

        has_next = results.has_next
        searched_post_tuples = results.items

        searched_posts = [post for post, _, _ in searched_post_tuples]

        return (has_next, searched_posts)

    def search_posts(
        self,
        user: User,
        isPreview: bool = True,
        page: int = 1,
        per_page: int = 10,
        search_dist: dict[str, str] = {},
    ) -> Tuple[bool, List[Dict[str, Union[str, int, bool, List]]]]:
        """
             Get posts based on the search criteria, including search_text, updated_time_filter, type_filter, tag_filter, and sort_by, based on the pagination parameters (page and per_page)
        Args:
            user (User): The user who is currently logged in.
            isPreview (bool): A flag to determine if the post is a preview.
            page (int): The page number of the post list.
            per_page (int): The number of the posts per page.
        Returns:
            Tuple[List[Dict[str, Union[str, int, bool, List]]]]: A tuple containing a boolean indicating if there are more posts and a list of post DTOs.
        """
        has_next, searched_posts = self._construct_search_query(
            page, per_page, search_dist
        )

        postDTOs = [
            PostDTO(post, post.postCreator, user, isPreview).to_dict()
            for post in searched_posts
        ]

        return has_next, postDTOs
