from datetime import datetime
import random
from faker import Faker
from enum import Enum

from app import db
from app.models.user import User
from app.models.post import Post, Status
from app.models.comment import Comment
from app.utils.helper import format_datetime
from app.utils.cliColor import Colors
from app.models.tag import Tag

fake = Faker()

# todo: upload picture to upload folder, gitignore the upload folder


def seeds():
    # recreate the database
    db.drop_all()
    db.create_all()
    print(Colors.fg.cyan, "Database recreated successfully!")

    # Create users
    print(Colors.fg.green, "Creating users...")
    for i in range(100):
        user = User(
            {
                "email": f"{fake.user_name()}@mmu.edu.my",
                "password": "password",
                "username": fake.user_name(),
                "avatar_url": "https://source.unsplash.com/random/80x80/?anonymous-id",
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
    from data import tags

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
    print(Colors.fg.green, "Creating posts...")
    users = User.query.all()
    for user in random.sample(users, 10):
        for _ in range(random.randint(1, 4)):
            post = Post(
                {
                    "title": fake.text(max_nb_chars=120),
                    "content": "\n".join(fake.paragraphs(nb=random.randint(2, 6))),
                    "image_url": f"https://source.unsplash.com/random/{random.randint(200, 800)}x{random.randint(200, 800)}",
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
        for _ in range(random.randint(0, 5)):
            post.tags.append(random.choice(tags))
            db.session.add(post)
            db.session.commit()
    print(Colors.fg.green, "-" * 50)
    print(Colors.fg.green, "Tags assigned to posts successfully!")

    # Create comments
    print(Colors.fg.green, "Creating comments...")
    posts = Post.query.all()
    for post in posts:
        for _ in range(random.randint(1, 6)):
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
    print(Colors.fg.green, "Creating replies...")
    comments = Comment.query.all()
    for comment in comments:
        for _ in range(random.randint(0, 5)):
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
