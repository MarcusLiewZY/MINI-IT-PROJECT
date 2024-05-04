import click
from datetime import datetime
from flask.cli import FlaskGroup

from app import app, db
from config import admin_users
from app.utils.cliColor import Colors
from app.utils.helper import format_datetime

cli = FlaskGroup(app)

# todo: custom the admin the cli
@cli.command("create_admin", help="Create admin user.")
@click.option(
    "--manual",
    "-m",
    is_flag=True,
    help="Create admin user using command line manually.",
)
@click.option(
    "--auto", "-a", is_flag=True, help="Create admin user with predefined admin infos."
)
def create_admin(manual, auto):
    import getpass
    from app.models.user import User
    from app.user.forms import AdminRegisterForm
    
    try:
        if manual:
            email = input("Enter email address: ")
            username = input("Enter your name: ")
            password = getpass.getpass("Enter password: ")
            confirm_password = getpass.getpass("Enter password again: ")
            
            form = AdminRegisterForm(
                email=email,
                username=username,
                password=password,
                confirm_password=confirm_password
            )
            if form.validate():
                user = User(
                    {   'email': form.email.data,
                        'username': form.username.data,
                        'password': form.password.data,
                        'is_admin': True,
                        'created_at': format_datetime(datetime.now())
                    }
                )

                db.session.add(user)
                db.session.commit()
                print(Colors.fg.green, f"Admin with email {form.email.data} created successfully!")
            else:
                raise Exception("Invalid input.")

        elif auto:
            for admin_data in admin_users:
                user = User(
                    {
                        "email": admin_data["email"],
                        "username": admin_data["username"],
                        "password": admin_data["password"],
                        "is_admin": True,
                        "created_at": format_datetime(datetime.now()),
                    }
                )
                db.session.add(user)
                db.session.commit()
                print(
                    Colors.fg.green,
                    f"Admin with email {admin_data["email"]} created successfully!",
                )
    except Exception as e:
        print(Colors.fg.red, "Couldn't create admin user.")
        print("Error", e)
        if form.errors:
            for field, errors in form.errors.items():
                for error in errors:
                    print(f"{field}: {error}")
# database
@cli.command("recreate_db")
def recreate_db():
    db.drop_all()
    db.create_all()
    db.session.commit()
    print(Colors.fg.cyan, "Database recreated successfully!")

@cli.command("delete_resource", help = "Delete resources from the database.")
@click.option("--user", is_flag = True, help = "Delete non-admin users.")
@click.option("--admin_user", is_flag = True, help = "Delete admin users.")
@click.option("--post", is_flag = True, help = "Delete posts.")
@click.option("--tag", is_flag = True, help = "Delete tags.")
def delete_resource(user, admin_user, post, tag):
    from app.models import User, Post, Tag, PostTag
    from sqlalchemy import delete
    try: 
        if user:
            User.query.filter(User.is_admin == False).delete()
            db.session.commit()
            print(Colors.fg.green, "Non-admin users deleted successfully!")
        elif admin_user:
            User.query.filter(User.is_admin == True).delete()
            db.session.commit()
            print(Colors.fg.green, "Admin users deleted successfully!")
        elif post:
            for post in Post.query.all():
                db.session.execute(delete(PostTag).where(PostTag.c.post_id == post.id))
                Post.query.filter(Post.id == post.id).delete()
            db.session.commit()
            print(Colors.fg.green, "Posts deleted successfully!")
        elif tag:
            for tag in Tag.query.all():
                db.session.execute(delete(PostTag).where(PostTag.c.tag_id == tag.id))
                Tag.query.filter(Tag.id == tag.id).delete()
            db.session.commit()
            print(Colors.fg.green, "Tags deleted successfully!")

    except Exception as e:
        print(Colors.fg.red, "Delete operations failed.")
        print("Error", e)

@cli.command("create_resource", help = "Add resources to the database.")
@click.option('--post', is_flag = True, help = "Add posts to the database.")
@click.option('--tag', is_flag = True, help = "Add post tags to the database.")
def create_resource(post, tag):
    from app.models import Post, Tag
    from constants import posts, tags
    
    try:
        if post:
            for post_data in posts:
                post = Post(
                    {
                        "title": post_data['title'],
                        "content": post_data['content'],
                        'image_url': post_data['image_url'],
                        'created_at': format_datetime(post_data['created_at'])
                    }
                )
                db.session.add(post)
                db.session.commit()
            print(Colors.fg.green, 'Posts added successfully!')
        elif tag:
            for tag_data in tags:
                tag = Tag(
                    {
                        'name': tag_data['name'],
                        'color': tag_data['color'],
                        'description': tag_data['description'],
                        'created_at': format_datetime(datetime.now())

                    }
                )
                db.session.add(tag)
                db.session.commit()
            print(Colors.fg.green, 'Tags added successfully!')

    except Exception as e:
        print(Colors.fg.red, "Couldn't create test data.")
        print("Error", e)

@cli.command('seeds', help = "Seed the database with dummy data.")
def seed():
    from seeds import seeds
    try:
        seeds()
        print(Colors.fg.green, '-'*50)
        print(Colors.fg.green, "Database seeded successfully!")
    except Exception as e:
        print(Colors.fg.red, "Database seeding failed.")
        print("Error", e)

if __name__ == "__main__":
    cli()
