import os
from datetime import datetime
from flask import url_for, redirect, flash, request, render_template
from flask_login import login_required, login_user, logout_user

from . import user
from app import oauth, db
from app.models import User
from app.utils.decorators import logout_required, development_only


@user.route("/sign-up")
@logout_required
def microsoft_login():
    microsoft_client = oauth.create_client("microsoft")
    redirect_uri = None

    redirect_uri = url_for("user.microsoft_auth", _external=True, _scheme="http")

    # if os.getenv("ENV") == "development":
    #     redirect_uri = url_for("user.microsoft_auth", _external=True)
    # elif os.getenv("ENV") == "production":
    #     redirect_uri = url_for("user.microsoft_auth", _external=True, _scheme="https")
    # else:
    #     raise Exception("Invalid Environment")

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

    avatar_url = None

    if avatar_response.status_code == 200:
        avatar_url = avatar_endpoint

    if user:
        login_user(user)

        # when the user sign up for the first time, the user.anon_no is None
        if user.anon_no is None:
            return redirect(url_for("main.community_guidelines"))

        flash("Successfully logged in", "success")
        return redirect(url_for("main.index"))
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
                "created_at": datetime.now(),
            }
        )
        db.session.add(user)
        db.session.commit()
        login_user(user)
        flash("Account created successfully", "success")
        return redirect(url_for("main.community_guidelines"))


@user.route("/sign-out")
@login_required
def logout():
    logout_user()
    return redirect(url_for("main.landing"))


@user.route("/faked-user-login", methods=["GET", "POST"])
@logout_required
@development_only
def faked_user_login():
    if request.method == "POST":
        email = request.form.get("email")

        if email is None:
            flash("Email is required.", "error")
            return redirect(url_for("main.landing"))

        email = request.form.get("email")
        user = User.query.filter_by(email=email).first()

        if user is None:
            flash("User not found.", "error")
            return redirect(url_for("main.landing"))

        login_user(user)
        return redirect(url_for("main.index"))

    return render_template("main/fakedUserLogin.html", user=None)
