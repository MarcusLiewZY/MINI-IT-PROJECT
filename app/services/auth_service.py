import os
from itsdangerous import URLSafeTimedSerializer
from flask_mail import Message

from app import mail


def generate_token(email):
    # create serializer for token generation
    serializer = URLSafeTimedSerializer(
        os.getenv("SECRET_KEY"), salt=os.getenv("SECURITY_PASSWORD_SALT")
    )

    return serializer.dumps(email, salt=os.getenv("SECURITY_PASSWORD_SALT"))


def confirm_token(token, expiration=3600):
    serializer = URLSafeTimedSerializer(
        os.getenv("SECRET_KEY"),
        salt=os.getenv("SECURITY_PASSWORD_SALT"),
    )

    try:
        email = serializer.loads(
            token,
            salt=os.getenv("SECURITY_PASSWORD_SALT"),
            max_age=expiration,
        )

        return email
    except Exception as e:
        print(e)
        return False


def send_mail(to, subject, template):
    msg = Message(
        subject,
        recipients=[to],
        html=template,
        sender=os.getenv("MAIL_DEFAULT_SENDER"),
    )

    mail.send(msg)
