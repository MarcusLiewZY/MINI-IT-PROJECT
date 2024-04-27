from flask.cli import FlaskGroup

from app import app, db

import getpass

cli = FlaskGroup(app)


# user management
# todo: compete create_admin cli
@cli.command("create_admin")
def create_admin():
    email = input("Enter email address: ")
    password = getpass.getpass("Enter password: ")
    confirm_password = getpass.getpass("Enter password again: ")
    if password != confirm_password:
        print("Passwords don't match")
    else:
        pass


# database
@cli.command("recreate_db")
def recreate_db():
    db.drop_all()
    db.create_all()
    db.session.commit()
    print("Database recreated successfully!")


if __name__ == "__main__":
    cli()
