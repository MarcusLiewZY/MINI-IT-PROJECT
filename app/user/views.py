from datetime import datetime
from flask import url_for, redirect, flash
from flask_login import login_required, login_user, logout_user

from app import oauth, db
from app.models import User
from . import user
from app.utils.decorators import logout_required
from app.utils.helper import format_datetime


@user.route("/sign-up")
@logout_required
def microsoft_login():
    microsoft_client = oauth.create_client("microsoft")
    redirect_uri = url_for("user.microsoft_auth", _external=True)

    return microsoft_client.authorize_redirect(redirect_uri)


@user.route("/sign-up/microsoft/callback")
@logout_required
def microsoft_auth():
    microsoft_client = oauth.create_client("microsoft")
    token = microsoft_client.authorize_access_token()
    resp = microsoft_client.get("me")
    user_info = resp.json()
    user = User.query.filter_by(email=user_info["mail"]).first()

    avatar_endpoint = (
        f"https://graph.microsoft.com/v1.0/users/{user_info['id']}/photo/$value"
    )

    avatar_response = microsoft_client.get(avatar_endpoint)

    if avatar_response.status_code == 200:
        avatar_url = avatar_endpoint
    else:
        avatar_url = None  # or a default avatar URL

    if user:
        login_user(user)
        flash("Successfully logged in", "success")
        return redirect(url_for("main.community_guidelines"))
    else:
        # check user email endwith mmu.edu.my
        if not user_info["mail"].endswith("mmu.edu.my"):
            flash("Please use your MMU email to sign up", "warning")
            return redirect(url_for("main.landing"))

        user = User(
            {
                "email": user_info["mail"],
                "password": user_info["mail"],
                "username": user_info["displayName"],
                "avatar_url": avatar_url,
                "created_at": format_datetime(datetime.now()),
            }
        )
        db.session.add(user)
        db.session.commit()
        login_user(user)
        flash("Account created successfully", "success")
        return redirect(url_for("main.index"))


@user.route("/sign-out")
@login_required
def logout():
    logout_user()
    return redirect(url_for("main.landing"))
