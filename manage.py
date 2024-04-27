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
    from app.models.user import User
    from datetime import datetime
    import getpass

    try:
        if manual:
            email = input("Enter email address: ")
            username = input("Enter your name: ")
            password = getpass.getpass("Enter password: ")
            confirm_password = getpass.getpass("Enter password again: ")
            if password != confirm_password:
                print(Colors.fg.red, "Passwords don't match.")
            else:
                user = User(
                    {
                        "email": email,
                        "username": username,
                        "password": password,
                        "is_admin": True,
                        "created_at": datetime.now(),
                    }
                )
                db.session.add(user)
                db.session.commit()
                print(
                    Colors.fg.green, f"Admin with email {email} created successfully!"
                )
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


# delete non-admin users
@cli.command("delete_users", help = "Delete all non-admin users")
def delete_users():
    from app.models.user import User
    try:
        User.query.filter(User.is_admin == False).delete()
        db.session.commit()
        print(Colors.fg.green, "Non-admin users deleted successfully!")
    except Exception as e:
        print(Colors.fg.red, "Couldn't delete non-admin users.")
        print("Error", e)        

# database
@cli.command("recreate_db")
def recreate_db():
    db.drop_all()
    db.create_all()
    db.session.commit()
    print(Colors.fg.cyan, "Database recreated successfully!")


if __name__ == "__main__":
    cli()
