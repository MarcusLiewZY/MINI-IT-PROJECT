import click
from flask.cli import FlaskGroup

from app import app, db
from config import admin_users
from app.utils.cliColor import Colors


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
    from datetime import datetime
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
                        'created_at': datetime.now()
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
                        "created_at": datetime.now(),
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

@cli.command("delete_db", help = "Delete resources from the database.")
@click.option("--user", is_flag = True, help = "Delete non-admin users.")
@click.option("--admin_user", is_flag = True, help = "Delete admin users.")
@click.option("--post", is_flag = True, help = "Delete posts.")
@click.option("--tag", is_flag = True, help = "Delete tags.")
def delete_db(user, admin_user, post, tag):
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

@cli.command("generate")
def generate():
    from app.models import Post, Tag
    from dummy import posts, tags

    try:
        post1 = Post(posts[0])
        post2 = Post(posts[1])
        post3 = Post(posts[2])

        tag1 = Tag(tags[0])
        tag2 = Tag(tags[1])
        tag3 = Tag(tags[2])
        tag4 = Tag(tags[3])

        post1.tags.append(tag1)  # Tag the first post with 'animals'
        post1.tags.append(tag4)  # Tag the first post with 'writing'
        post3.tags.append(tag3)  # Tag the third post with 'cooking'
        post3.tags.append(tag2)  # Tag the third post with 'tech'
        post3.tags.append(tag4)  # Tag the third post with 'writing'

        db.session.add_all([post1, post2, post3])
        db.session.add_all([tag1, tag2, tag3, tag4])
        db.session.commit()

        print(Colors.fg.green, "Test data created successfully!")

    except Exception as e:
        print(Colors.fg.red, "Couldn't create test data.")
        print("Error", e)

@cli.command("init_app")
def init_app():
    from flask import current_app
    
    try:
        _ = current_app.config
        print(Colors.fg.green, "App initialized successfully!")
        return True
    except RuntimeError:
        print(Colors.fg.red, "App not initialized.")
        return False

if __name__ == "__main__":
    cli()
