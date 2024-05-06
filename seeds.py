from datetime import datetime
import random
from faker import Faker

from app import app
from app import db
from app.models.user import User
from app.models.post import Post, Status
from app.models.comment import Comment
from app.models.postNotification import PostNotification
from app.models.commentNotification import CommentNotification
from app.models.tag import Tag
from app.utils.helper import format_datetime, upload_image
from app.utils.cliColor import Colors

fake = Faker()

NUM_USERS = 100

NUM_USERS_CREATE_POST = 10
MIN_POSTS_PER_USER = 1 
MAX_POSTS_PER_USER = 4 

MIN_POST_WIDTH = 400
MAX_POST_WIDTH = 1000
MIN_POST_HEIGHT = 400
MAX_POST_HEIGHT = 1000

MIN_TAGS_PER_POST = 0
MAX_TAGS_PER_POST = 5

MIN_LIKES_PER_POST = 0
MAX_LIKES_PER_POST = 20

MIN_BOOKMARKS_PER_POST = 0
MAX_BOOKMARKS_PER_POST = 20

MIN_COMMENTS_PER_POST = 1
MAX_COMMENTS_PER_POST = 6

MIN_REPLIES_PER_COMMENT = 0
MAX_REPLIES_PER_COMMENT = 5

MIN_LIKES_PER_COMMENT = 0
MAX_LIKES_PER_COMMENT = 20

MIN_NOTIFICATIONS_PER_POST = 0
MAX_NOTIFICATIONS_PER_POST = 3

MIN_NOTIFICATIONS_PER_COMMENT = 0
MAX_NOTIFICATIONS_PER_COMMENT = 2


def seeds():
    # recreate the database
    db.drop_all()
    db.create_all()
    print(Colors.fg.cyan, "Database recreated successfully!")

    # Create users
    print(Colors.fg.green, "Creating users...")
    for i in range(NUM_USERS):
        user_name = fake.user_name()
        avatar_url = "https://source.unsplash.com/random/80x80/?anonymous-id"
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
                "is_admin": False,
                "created_at": format_datetime(
                    fake.date_between(
                        start_date=datetime(2020, 1, 1),
                        end_date=datetime(2021, 12, 31),
                    )
                ),
            }
        )
        print(Colors.fg.green, f"User {i+1} created")
        db.session.add(user)
        db.session.commit()
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
                "created_at": format_datetime(
                    datetime.strptime("2018-01-01", "%Y-%m-%d")
                ),
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
    for user in random.sample(users, NUM_USERS_CREATE_POST):
        for _ in range(random.randint(MIN_POSTS_PER_USER, MAX_POSTS_PER_USER)):
            image_url = f"https://source.unsplash.com/random/{random.randint(MIN_POST_WIDTH, MAX_POST_WIDTH)}x{random.randint(MIN_POST_HEIGHT, MAX_POST_HEIGHT)}"
            cloudinary_image_url = upload_image(
                image_url, app.config["CLOUDINARY_POST_IMAGE_FOLDER"]
            )
            post = Post(
                {
                    "title": fake.text(max_nb_chars=120),
                    "content": "\n".join(fake.paragraphs(nb=random.randint(2, 6))),
                    "image_url": cloudinary_image_url,
                    "created_at": format_datetime(
                        fake.date_between(
                            start_date=datetime.strptime(
                                user.created_at, "%Y-%m-%d %H:%M:%S"
                            ),
                            end_date=datetime(2021, 12, 31),
                        )
                    ),
                }
            )
            post.status = Status.APPROVED
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
        for _ in range(random.randint(MIN_TAGS_PER_POST, MAX_TAGS_PER_POST)):
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
        for user in random.sample(users, random.randint(MIN_LIKES_PER_POST, MAX_LIKES_PER_POST)):
            post.liked_by.append(user)
            db.session.add(post)
            db.session.commit()
    print(Colors.fg.green, "-" * 50)
    print(Colors.fg.green, "Post likes created successfully!")

    # Create post bookmarks (many-to-many relationship)
    # note that each user can bookmark at most 20 posts
    print(Colors.fg.green, "Creating post bookmarks...")
    posts = Post.query.all()
    users = User.query.all()
    for post in posts:
        for user in random.sample(users, random.randint(MIN_BOOKMARKS_PER_POST, MAX_BOOKMARKS_PER_POST)):
            post.bookmarked_by.append(user)
            db.session.add(post)
            db.session.commit()
    print(Colors.fg.green, "-" * 50)
    print(Colors.fg.green, "Post bookmarks created successfully!")

    # Create comments
    # each post has 1-6 comments
    print(Colors.fg.green, "Creating comments...")
    posts = Post.query.all()
    for post in posts:
        for _ in range(random.randint(MIN_COMMENTS_PER_POST, MAX_COMMENTS_PER_POST)):
            comment = Comment(
                {
                    "content": fake.text(),
                    "created_at": format_datetime(
                        fake.date_between(
                            start_date=datetime.strptime(
                                post.created_at, "%Y-%m-%d %H:%M:%S"
                            ),
                            end_date=datetime(2022, 12, 31),
                        )
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
    print(Colors.fg.green, "Creating replies...")
    comments = Comment.query.all()
    for comment in comments:
        for _ in range(random.randint(MIN_REPLIES_PER_COMMENT, MAX_REPLIES_PER_COMMENT)):
            reply_comment = Comment(
                {
                    "content": fake.text(),
                    "created_at": format_datetime(
                        fake.date_between(
                            start_date=datetime.strptime(
                                comment.created_at, "%Y-%m-%d %H:%M:%S"
                            ),
                            end_date=datetime(2023, 12, 31),
                        )
                    ),
                }
            )
            reply_comment.user_id = random.choice(users).id
            reply_comment.post_id = comment.post_id
            reply_comment.replied_comment_id = comment.id
            db.session.add(reply_comment)
        db.session.commit()
        print(
            Colors.fg.green,
            f"Replies created for comment {comment.content} successfully!",
        )
    print(Colors.fg.green, "-" * 50)
    print(Colors.fg.green, "Replies created successfully!")

    # Create comment likes (many-to-many relationship)
    # each user can like at most 20 comments
    print(Colors.fg.green, "Creating comment likes...")
    comments = Comment.query.all()
    users = User.query.all()
    for comment in comments:
        for user in random.sample(users, random.randint(MIN_LIKES_PER_COMMENT, MAX_LIKES_PER_COMMENT)):
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
        for _ in range(random.randint(MIN_NOTIFICATIONS_PER_POST, MAX_NOTIFICATIONS_PER_POST)):
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
            num_notifications = min(random.randint(MIN_NOTIFICATIONS_PER_COMMENT, MAX_NOTIFICATIONS_PER_COMMENT), len(comment.replies))
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
