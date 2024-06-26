import os
import config
from dotenv import load_dotenv

from flask import Flask
from flask_login import LoginManager
from flask_bcrypt import Bcrypt
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from flask_mail import Mail
from flask_wtf.csrf import CSRFProtect
from authlib.integrations.flask_client import OAuth
import cloudinary

load_dotenv()

app = Flask(__name__)  # src
app.static_folder = "static"
app.template_folder = "templates"


# Configuration
if os.getenv("ENV") == "production":
    app.config.from_object(config.ProductionConfig)
elif os.getenv("ENV") == "testing":
    app.config.from_object(config.TestingConfig)
else:
    app.config.from_object(config.DevelopmentConfig)


# Initialization
csrf = CSRFProtect(app)
login_manager = LoginManager()
login_manager.init_app(app)
bcrypt = Bcrypt(app)
db = SQLAlchemy(app)
migrate = Migrate(app, db)
mail = Mail(app)

# OAuth setup
oauth = OAuth(app)
# google = oauth.register(
#     name="google",
#     client_id=os.getenv("GOOGLE_CLIENT_ID"),
#     client_secret=os.getenv("GOOGLE_CLIENT_SECRET"),
#     access_token_url="https://accounts.google.com/o/oauth2/token",
#     access_token_params=None,
#     authorize_url="https://accounts.google.com/o/oauth2/auth",
#     authorize_params=None,
#     api_base_url="https://www.googleapis.com/oauth2/v1/",
#     userinfo_endpoint="https://openidconnect.googleapis.com/v1/userinfo",  # This is only needed if using openId to fetch user info
#     client_kwargs={"scope": "email profile"},
#     server_metadata_url="https://accounts.google.com/.well-known/openid-configuration",
# )

microsoft = oauth.register(
    name="microsoft",
    client_id=os.getenv("MICROSOFT_CLIENT_ID"),
    client_secret=os.getenv("MICROSOFT_CLIENT_SECRET"),
    access_token_url="https://login.microsoftonline.com/common/oauth2/v2.0/token",
    access_token_params=None,
    authorize_url="https://login.microsoftonline.com/common/oauth2/v2.0/authorize",
    authorize_params=None,
    api_base_url="https://graph.microsoft.com/v1.0/",
    userinfo_endpoint="https://graph.microsoft.com/v1.0/me",  # This is only needed if using openId to fetch user info
    client_kwargs={"scope": "User.Read"},
)

# Cloudinary setup
cloudinary.config(
    cloud_name=os.getenv("CLOUDINARY_CLOUD_NAME"),
    api_key=os.getenv("CLOUDINARY_API_KEY"),
    api_secret=os.getenv("CLOUDINARY_API_SECRET"),
)


# Jinja custom filters
from app.utils.customFilter import preserve_line_breaks

app.jinja_env.filters["line_breaks"] = preserve_line_breaks

# Blueprints registration
from app.main.views import main
from app.auth.views import user
from app.admin.views import admin
from app.post.views import post
from app.me.views import me_bp
from app.notification.views import notification
from app.faq.views import faq
from app.about.views import about_bp

from app.api import api

app.register_blueprint(main)
app.register_blueprint(user)
app.register_blueprint(admin)
app.register_blueprint(post)
app.register_blueprint(me_bp)
app.register_blueprint(notification)
app.register_blueprint(faq)

app.register_blueprint(about_bp)

app.register_blueprint(api)
