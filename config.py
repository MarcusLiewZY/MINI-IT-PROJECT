import os
from dotenv import load_dotenv

load_dotenv()

DATABASE_URI = os.getenv("DATABASE_URL")
if DATABASE_URI.startswith("postgres://"):
    DATABASE_URI = DATABASE_URI.replace("postgres://", "postgresql://", 1)


class Config(object):
    DEBUG = False
    TESTING = False
    CSRF_ENABLED = True
    SECRET_KEY = os.getenv("SECRET_KEY", default="this-is-the-default-secret-key")
    SQLALCHEMY_DATABASE_URI = DATABASE_URI
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    BCRYPT_LOG_ROUNDS = 13
    WTF_CSRF_ENABLED = True
    DEBUG_TB_ENABLED = False
    # configuration option for the DebugToolbarExtension in Flask
    DEBUG_TB_INTERCEPT_REDIRECTS = False
    SECURITY_PASSWORD_SALT = os.getenv(
        "SECURITY_PASSWORD_SALT", default="very-important"
    )

    # Flask-Mail configuration
    # MAIL_DEFAULT_SENDER = "MMU Confessions <noreply@mmu-confession.com>"
    # MAIL_SERVER = "smtp.gmail.com"
    # MAIL_PORT = 587
    # MAIL_USE_TLS = True
    # MAIL_USE_SSL = False
    # MAIL_DEBUG = False
    # MAIL_USERNAME = os.getenv("EMAIL_USER")
    # MAIL_PASSWORD = "iahx wpyu mtzl mxbv"
    # MAIL_SUPRESS_SEND = False

    # Flask-Mail configuration
    MAIL_DEFAULT_SENDER = "MMU Confessions <1221105751@student.mmu.edu.my>"
    MAIL_SERVER = "mail.smtp2go.com"  # SMTP2GO SMTP server
    MAIL_PORT = 2525
    MAIL_USE_TLS = True
    MAIL_USE_SSL = False
    MAIL_USERNAME = "student.mmu.edu.my"
    MAIL_PASSWORD = "o1cncP9r7oaNJj7s"
    MAIL_SUPRESS_SEND = False

    # Cloudinary configuration
    CLOUDINARY_POST_IMAGE_FOLDER = "mmu-confession/dev/post-images"
    CLOUDINARY_AVATAR_IMAGE_FOLDER = "mmu-confession/dev/avatar-images"


class DevelopmentConfig(Config):
    DEVELOPMENT = True
    DEBUG = True
    WTF_CSRF_ENABLED = False
    DEBUG_TB_ENABLED = True


class TestingConfig(Config):
    TESTING = True
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = "sqlite:///testdb.sqlite"
    BCRYPT_LOG_ROUNDS = 1
    WTF_CSRF_ENABLED = False


class ProductionConfig(Config):
    DEBUG = False
    DEBUG_TB_ENABLED = True
