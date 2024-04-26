import os
from dotenv import load_dotenv
from flask import Flask
from flask_login import LoginManager
from flask_bcrypt import Bcrypt
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy

from app.models import User

load_dotenv()

app = Flask(__name__)  # src
app.config.from_object(os.getenv("APP_SETTINGS"))  # configuration
app.static_folder = "static"

# Initialization
login_manager = LoginManager()
login_manager.init_app(app)
bcrypt = Bcrypt(app)
db = SQLAlchemy(app)
migrate = Migrate(app, db)

# Blueprints registration
from app.main.views import main

app.register_blueprint(main)

# mock user
users = {"foo@bar.tld": {"password": "secret"}}


@login_manager.user_loader
def user_loader(email):
    if email not in users:
        return

    user = User()
    user.id = email
    return user
