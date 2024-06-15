from sqlalchemy import insert
from datetime import datetime
import random
from faker import Faker

from app import app
from app import db
from app.models.user import User, PostLike, PostBookmark
from app.models.post import Post, PostStatus
from app.models.comment import Comment
from app.models.postNotification import PostNotification
from app.models.commentNotification import CommentNotification
from app.models.tag import Tag
from app.utils.helper import upload_image
from app.utils.cliColor import Colors

fake = Faker()


class SeedConfig(object):
    def __init__(self) -> None:
        pass

    def set_config(self, seeding_level):
        if seeding_level == "simple":
            self._set_simple_seeding_config()
        elif seeding_level == "medium":
            self._set_medium_seeding_config()
        elif seeding_level == "complex":
            self._set_complex_seeding_config()
        else:
            raise ValueError(
                "Invalid seeding level. Please choose from 'simple', 'medium', 'complex'"
            )

    def _set_simple_seeding_config(self):
        self.NUM_USERS = 10
        self.NUM_USERS_CREATE_POST = 5
        self.MIN_POSTS_PER_USER = 1
        self.MAX_POSTS_PER_USER = 2
        self.MIN_POST_WIDTH = 400
        self.MAX_POST_WIDTH = 1000
        self.MIN_POST_HEIGHT = 400
        self.MAX_POST_HEIGHT = 1000
        self.MIN_TAGS_PER_POST = 0
        self.MAX_TAGS_PER_POST = 5
        self.MIN_LIKES_PER_POST = 0
        self.MAX_LIKES_PER_POST = 5
        self.MIN_BOOKMARKS_PER_POST = 0
        self.MAX_BOOKMARKS_PER_POST = 5
        self.MIN_COMMENTS_PER_POST = 1
        self.MAX_COMMENTS_PER_POST = 3
        self.MIN_REPLIES_PER_COMMENT = 0
        self.MAX_REPLIES_PER_COMMENT = 2
        self.MIN_LIKES_PER_COMMENT = 0
        self.MAX_LIKES_PER_COMMENT = 5
        self.MIN_NOTIFICATIONS_PER_POST = 0
        self.MAX_NOTIFICATIONS_PER_POST = 2
        self.MIN_NOTIFICATIONS_PER_COMMENT = 0
        self.MAX_NOTIFICATIONS_PER_COMMENT = 1

    def _set_medium_seeding_config(self):
        self.NUM_USERS = 50
        self.NUM_USERS_CREATE_POST = 10
        self.MIN_POSTS_PER_USER = 1
        self.MAX_POSTS_PER_USER = 2
        self.MIN_POST_WIDTH = 400
        self.MAX_POST_WIDTH = 1000
        self.MIN_POST_HEIGHT = 400
        self.MAX_POST_HEIGHT = 1000
        self.MIN_TAGS_PER_POST = 0
        self.MAX_TAGS_PER_POST = 5
        self.MIN_LIKES_PER_POST = 0
        self.MAX_LIKES_PER_POST = 10
        self.MIN_BOOKMARKS_PER_POST = 0
        self.MAX_BOOKMARKS_PER_POST = 10
        self.MIN_COMMENTS_PER_POST = 1
        self.MAX_COMMENTS_PER_POST = 4
        self.MIN_REPLIES_PER_COMMENT = 0
        self.MAX_REPLIES_PER_COMMENT = 3
        self.MIN_LIKES_PER_COMMENT = 0
        self.MAX_LIKES_PER_COMMENT = 10
        self.MIN_NOTIFICATIONS_PER_POST = 0
        self.MAX_NOTIFICATIONS_PER_POST = 3
        self.MIN_NOTIFICATIONS_PER_COMMENT = 0
        self.MAX_NOTIFICATIONS_PER_COMMENT = 2

    def _set_complex_seeding_config(self):
        self.NUM_USERS = 100
        self.NUM_USERS_CREATE_POST = 10
        self.MIN_POSTS_PER_USER = 1
        self.MAX_POSTS_PER_USER = 4
        self.MIN_POST_WIDTH = 400
        self.MAX_POST_WIDTH = 1000
        self.MIN_POST_HEIGHT = 400
        self.MAX_POST_HEIGHT = 1000
        self.MIN_TAGS_PER_POST = 0
        self.MAX_TAGS_PER_POST = 5
        self.MIN_LIKES_PER_POST = 0
        self.MAX_LIKES_PER_POST = 20
        self.MIN_BOOKMARKS_PER_POST = 0
        self.MAX_BOOKMARKS_PER_POST = 20
        self.MIN_COMMENTS_PER_POST = 1
        self.MAX_COMMENTS_PER_POST = 6
        self.MIN_REPLIES_PER_COMMENT = 0
        self.MAX_REPLIES_PER_COMMENT = 5
        self.MIN_LIKES_PER_COMMENT = 0
        self.MAX_LIKES_PER_COMMENT = 20
        self.MIN_NOTIFICATIONS_PER_POST = 0
        self.MAX_NOTIFICATIONS_PER_POST = 3
        self.MIN_NOTIFICATIONS_PER_COMMENT = 0
        self.MAX_NOTIFICATIONS_PER_COMMENT = 2


def seeds(seed_config: SeedConfig):

    # recreate the database
    db.drop_all()
    db.create_all()
    print(Colors.fg.cyan, "Database recreated successfully!")

    # Create users
    print(Colors.fg.green, "Creating users...")
    for i in range(seed_config.NUM_USERS):
        user_name = fake.user_name()
        avatar_url = "https://source.unsplash.com/random/80x80/?anonymous-id"
        cloudinary_avatar_url = upload_image(
            avatar_url, app.config["CLOUDINARY_AVATAR_IMAGE_FOLDER"]
        )

        if cloudinary_avatar_url is None:
            avatar_url = "https://picsum.photos/80/80"
            cloudinary_avatar_url = upload_image(
                avatar_url, app.config["CLOUDINARY_AVATAR_IMAGE_FOLDER"]
            )

        user = User(
            {
                "email": f"{user_name}@mmu.edu.my",
                "password": fake.password(),
                "username": user_name,
                "avatar_url": cloudinary_avatar_url,
                "campus": random.choice(["CYBERJAYA", "MALACCA"]),
                "is_confirmed": True,
                "is_admin": False,
                "created_at": fake.date_between(
                    start_date=datetime(2020, 1, 1),
                    end_date=datetime(2021, 12, 31),
                ),
            }
        )
        print(Colors.fg.green, f"User {i+1} created")
        db.session.add(user)
        db.session.commit()

        user.anon_no = User.generate_anon_no()

    print(Colors.fg.green, "-" * 50)
    print(Colors.fg.green, "Users created successfully!")

    # Create tags
    # the tags are created at 1-1-2018
    from constants import tags

    print(Colors.fg.green, "Creating tags...")
    for tag_data in tags:
        tag = Tag(
            {
                "name": tag_data["name"],
                "color": tag_data["color"],
                "description": tag_data["description"],
                "created_at": datetime(2018, 1, 1),
            }
        )
        db.session.add(tag)
        db.session.commit()
    print(Colors.fg.green, "-" * 50)
    print(Colors.fg.green, "Tags created successfully!")

    # Create posts
    # 10 users have posts
    # each user creates 1-4 posts
    print(Colors.fg.green, "Creating posts...")
    users = User.query.all()
    for user in random.sample(users, seed_config.NUM_USERS_CREATE_POST):
        for _ in range(
            random.randint(
                seed_config.MIN_POSTS_PER_USER, seed_config.MAX_POSTS_PER_USER
            )
        ):
            image_url = f"https://source.unsplash.com/random/{random.randint(seed_config.MIN_POST_WIDTH, seed_config.MAX_POST_WIDTH)}x{random.randint(seed_config.MIN_POST_HEIGHT, seed_config.MAX_POST_HEIGHT)}"

            cloudinary_image_url = upload_image(
                image_url, app.config["CLOUDINARY_POST_IMAGE_FOLDER"]
            )

            if cloudinary_image_url is None:
                image_url = f"https://picsum.photos/{random.randint(seed_config.MIN_POST_WIDTH, seed_config.MAX_POST_WIDTH)}/{random.randint(seed_config.MIN_POST_HEIGHT, seed_config.MAX_POST_HEIGHT)}"
                cloudinary_image_url = upload_image(
                    image_url, app.config["CLOUDINARY_POST_IMAGE_FOLDER"]
                )

            post = Post(
                {
                    "title": fake.text(max_nb_chars=120),
                    "content": "\n".join(fake.paragraphs(nb=random.randint(2, 6))),
                    "image_url": cloudinary_image_url,
                    "created_at": fake.date_between(
                        start_date=user.created_at,
                        end_date=datetime(2021, 12, 31),
                    ),
                }
            )
            post.status = PostStatus.APPROVED
            post.user_id = user.id
            db.session.add(post)
        db.session.commit()
        print(Colors.fg.green, f"Posts created for user {user.username} successfully!")
    print(Colors.fg.green, "-" * 50)
    print(Colors.fg.green, "Posts created successfully!")

    # Assign tags to posts (note each post can have at most 5 tags)
    posts = Post.query.all()
    tags = Tag.query.all()

    print(Colors.fg.green, "Assigning tags to posts...")
    for post in posts:
        for _ in range(
            random.randint(seed_config.MIN_TAGS_PER_POST, seed_config.MAX_TAGS_PER_POST)
        ):
            post.tags.append(random.choice(tags))
            db.session.add(post)
            db.session.commit()
    print(Colors.fg.green, "-" * 50)
    print(Colors.fg.green, "Tags assigned to posts successfully!")

    # Create post likes (many-to-many relationship)
    # note that each user can like at most 20 posts
    print(Colors.fg.green, "Creating post likes...")
    posts = Post.query.all()
    users = User.query.all()
    for post in posts:
        for user in random.sample(
            users,
            random.randint(
                seed_config.MIN_LIKES_PER_POST, seed_config.MAX_LIKES_PER_POST
            ),
        ):
            created_at = fake.date_between(
                start_date=post.updated_at,
                end_date=datetime(2023, 12, 31),
            )
            liked_post_user = insert(PostLike).values(
                user_id=user.id, post_id=post.id, created_at=created_at
            )
            db.session.execute(liked_post_user)
            db.session.commit()
    print(Colors.fg.green, "-" * 50)
    print(Colors.fg.green, "Post likes created successfully!")

    # Create post bookmarks (many-to-many relationship)
    # note that each user can bookmark at most 20 posts
    print(Colors.fg.green, "Creating post bookmarks...")
    posts = Post.query.all()
    users = User.query.all()
    for post in posts:
        for user in random.sample(
            users,
            random.randint(
                seed_config.MIN_BOOKMARKS_PER_POST, seed_config.MAX_BOOKMARKS_PER_POST
            ),
        ):
            created_at = fake.date_between(
                start_date=post.updated_at,
                end_date=datetime(2023, 12, 31),
            )

            bookmarked_post_user = insert(PostBookmark).values(
                user_id=user.id, post_id=post.id, created_at=created_at
            )

            db.session.execute(bookmarked_post_user)
            db.session.commit()
    print(Colors.fg.green, "-" * 50)
    print(Colors.fg.green, "Post bookmarks created successfully!")

    # Create comments
    # each post has 1-6 comments
    print(Colors.fg.green, "Creating comments...")
    posts = Post.query.all()
    for post in posts:
        for _ in range(
            random.randint(
                seed_config.MIN_COMMENTS_PER_POST, seed_config.MAX_COMMENTS_PER_POST
            )
        ):
            comment = Comment(
                {
                    "content": fake.text(),
                    "created_at": fake.date_between(
                        start_date=post.created_at,
                        end_date=datetime(2022, 12, 31),
                    ),
                }
            )
            comment.user_id = random.choice(users).id
            comment.post_id = post.id
            db.session.add(comment)
        db.session.commit()
        print(Colors.fg.green, f"Comments created for post {post.title} successfully!")
    print(Colors.fg.green, "-" * 50)
    print(Colors.fg.green, "Comments created successfully!")

    # Create replies
    # each comment has 0-5 replies
    # the comment level can up to 5
    # the comment level of the comments of the post is 1
    # the comment level of the replies of the comments is 2
    # the comment level of the replies of the replies of the comments is 3 and so on

    MIN_COMMENT_LEVEL = 2
    MAX_COMMENT_LEVEL = 5

    def create_replies(comment, level, max_level):
        # base case
        if level == max_level:
            return

        for _ in range(
            random.randint(
                seed_config.MIN_REPLIES_PER_COMMENT, seed_config.MAX_REPLIES_PER_COMMENT
            )
        ):
            reply_comment = Comment(
                {
                    "content": fake.text(),
                    "created_at": fake.date_between(
                        start_date=comment.created_at,
                        end_date=datetime(2023, 12, 31),
                    ),
                }
            )
            reply_comment.user_id = random.choice(users).id
            reply_comment.post_id = comment.post_id
            reply_comment.replied_comment_id = comment.id
            db.session.add(reply_comment)
            create_replies(reply_comment, level + 1, max_level)

        db.session.commit()

    print(Colors.fg.green, "Creating replies...")
    comments = Comment.query.all()
    for comment in comments:
        max_level = random.randint(MIN_COMMENT_LEVEL, MAX_COMMENT_LEVEL)
        create_replies(comment, 1, max_level)
    print(Colors.fg.green, "-" * 50)
    print(Colors.fg.green, "Replies created successfully!")

    # Create comment likes (many-to-many relationship)
    # each user can like at most 20 comments
    print(Colors.fg.green, "Creating comment likes...")
    comments = Comment.query.all()
    users = User.query.all()
    for comment in comments:
        for user in random.sample(
            users,
            random.randint(
                seed_config.MIN_LIKES_PER_COMMENT, seed_config.MAX_LIKES_PER_COMMENT
            ),
        ):
            comment.liked_by.append(user)
            db.session.add(comment)
            db.session.commit()
    print(Colors.fg.green, "-" * 50)
    print(Colors.fg.green, "Comment likes created successfully!")

    # Create post notifications
    # what is post notification?
    # - when others comment on the user's post, the user will receive a notification. This is a post notification.
    # user_id, post_id, unread_comment_id
    # for each post, create 0-3 post notifications

    print(Colors.fg.green, "Creating post notifications...")
    posts = Post.query.all()
    users = User.query.all()
    for post in posts:
        for _ in range(
            random.randint(
                seed_config.MIN_NOTIFICATIONS_PER_POST,
                seed_config.MAX_NOTIFICATIONS_PER_POST,
            )
        ):
            unread_comment = random.choice(post.comments)
            post_notification = PostNotification(
                {
                    "is_read": False,
                    "user_id": post.user_id,
                    "post_id": post.id,
                    "unread_comment_id": unread_comment.id,
                    "created_at": unread_comment.created_at,
                }
            )
            db.session.add(post_notification)
        db.session.commit()
    print(Colors.fg.green, "-" * 50)
    print(Colors.fg.green, "Post notifications created successfully!")

    # Create comment notifications
    # what is comment notification?
    # - when others reply to the user's comment, the user will receive a notification. This is a comment notification.
    # user_id, comment_id, unread_comment_id
    # for each comment, create 0-2 comment notifications

    print(Colors.fg.green, "Creating comment notifications...")
    comments = Comment.query.all()
    users = User.query.all()
    for comment in comments:
        if comment.replies:
            num_notifications = min(
                random.randint(
                    seed_config.MIN_NOTIFICATIONS_PER_COMMENT,
                    seed_config.MAX_NOTIFICATIONS_PER_COMMENT,
                ),
                len(comment.replies),
            )
            for unread_comment in random.sample(comment.replies, num_notifications):
                comment_notification = CommentNotification(
                    {
                        "is_read": False,
                        "user_id": comment.user_id,
                        "comment_id": comment.id,
                        "unread_comment_id": unread_comment.id,
                        "created_at": unread_comment.created_at,
                    }
                )
                db.session.add(comment_notification)
            db.session.commit()
    print(Colors.fg.green, "-" * 50)
    print(Colors.fg.green, "Comment notifications created successfully!")
