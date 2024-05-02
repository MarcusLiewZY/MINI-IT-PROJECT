import time
from datetime import datetime
from flask import url_for, redirect, flash
from flask_login import login_required, login_user, logout_user

from app import oauth, db
from app.models import User
from . import user
from app.utils.decorators import logout_required


@user.route("/sign-up")
@logout_required
def google_login():
    google_client = oauth.create_client("google")
    redirect_uri = url_for("user.google_auth", _external=True)

    return google_client.authorize_redirect(redirect_uri)


@user.route("/sign-up/google/callback")
@logout_required
def google_auth():
    google_client = oauth.create_client("google")
    token = google_client.authorize_access_token()
    resp = google_client.get("userinfo")
    user_info = resp.json()
    user = User.query.filter_by(email=user_info["email"]).first()

    if user:
        login_user(user)
        flash("Successfully logged in", "success")
        return redirect(url_for("main.community_guideline"))
    else:
        # check user email endwith mmu.edu.my
        if not user_info["email"].endswith("mmu.edu.my"):
            flash("Please use your MMU email to sign up", "warning")
            return redirect(url_for("main.landing"))

        user = User(
            {
                "email": user_info["email"],
                "password": user_info["email"],
                "username": user_info["name"],
                "avatar_url": user_info["picture"],
                "created_at": datetime.now(),
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
