import os
import click
from datetime import datetime
from flask.cli import FlaskGroup

from app import app, db
from app.utils.cliColor import Colors

cli = FlaskGroup(app)


@cli.command(
    "role",
    help="Change user role with the given gmail. Either from admin to non-admin or vice versa.",
)
@click.option("--admin", is_flag=True, help="Change user role to admin.")
@click.option(
    "--non_admin", is_flag=True, help="Change user role from admin to non-admin."
)
def change_user_role(admin, non_admin):
    from app.models.user import User

    try:
        email = input("Enter email address: ")
        user = User.query.filter(User.email == email).first()

        if not user:
            print(Colors.fg.red, f"User with email {email} not found.")
            return

        if admin:
            user.is_admin = True
            user.updated_at = datetime.now()
            db.session.commit()
            print(Colors.fg.green, f"User with email {email} is now an admin.")
        elif non_admin:
            user.is_admin = False
            user.updated_at = datetime.now()
            db.session.commit()
            print(Colors.fg.green, f"User with email {email} is now a non-admin.")

    except Exception as e:
        print(Colors.fg.red, "Couldn't change user role.")
        print("Error", e)


# database
@cli.command("recreate_db")
def recreate_db():
    db.drop_all()
    db.create_all()
    db.session.commit()
    print(Colors.fg.cyan, "Database recreated successfully!")


@cli.command("seeds", help="Seed the database with dummy data.")
@click.option(
    "--simple",
    is_flag=True,
    help="Seed the database with simple seeding configuration.",
)
@click.option(
    "--medium",
    is_flag=True,
    help="Seed the database with medium seeding configuration.",
)
@click.option(
    "--complex",
    is_flag=True,
    help="Seed the database with complex seeding configuration.",
)
def seed(simple, medium, complex):
    """
    By default, seeds the database with simple seeding configuration.
    """

    from seeds import seeds, SeedConfig

    try:
        seed_config = SeedConfig()

        if medium:
            seed_config.set_config("medium")
        elif complex:
            seed_config.set_config("complex")
        else:
            seed_config.set_config("simple")

        seeds(seed_config=seed_config)

        print(Colors.fg.green, "-" * 50)
        print(Colors.fg.green, "Database seeded successfully!")
    except Exception as e:
        print(Colors.fg.red, "Database seeding failed.")
        print("Error", e)


@cli.command("test", help="Test any functionality.")
def test():
    pass


if __name__ == "__main__":
    mode = os.getenv("ENV", default="development")

    if mode == "development":
        cli()
    else:
        from waitress import serve

        serve(app, host="0.0.0.0", port=8080)
