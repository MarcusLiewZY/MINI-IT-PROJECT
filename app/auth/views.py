from datetime import datetime
from flask import url_for, redirect, flash, request, render_template
from flask_login import login_user, logout_user, current_user


from . import user
from app import bcrypt, db
from app.models import User
from app.auth.forms import (
    RegisterForm,
    LoginForm,
    ForgotPasswordForm,
    ResetPasswordForm,
)
from app.services.auth_service import confirm_token, generate_token, send_mail
from app.utils.decorators import login_required, logout_required, development_only


@user.route("/sign-up", methods=["GET", "POST"])
@logout_required
def sign_up():

    form = RegisterForm(request.form)

    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()

        if user:
            flash("Email already registered, please sign in", "warning")
            return redirect(url_for("user.sign_in"))

        user = User(
            {
                "email": form.email.data,
                "password": form.password.data,
                "username": form.email.data.split("@")[0],
                "created_at": datetime.now(),
            }
        )

        db.session.add(user)
        db.session.commit()

        token = generate_token(user.email)
        confirm_url = url_for(
            "user.confirm_email", token=token, _external=True
        )  # external=True to get the full url
        html = render_template("auth/confirmEmail.html", confirm_url=confirm_url)
        subject = "Please confirm your email"
        send_mail(user.email, subject, html)

        login_user(user)

        flash("A confirmation email has been sent via email.", "success")

        return redirect(url_for("user.inactive"))

    return render_template("auth/signUp.html", form=form)


@user.route("/sign-in", methods=["GET", "POST"])
@logout_required
def sign_in():
    form = LoginForm(request.form)

    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()

        if not user:
            flash("Invalid email", "error")
            return redirect(url_for("user.sign_in"))

        if bcrypt.check_password_hash(user.password, form.password.data) == False:
            flash("Invalid password", "error")
            return redirect(url_for("user.sign_in"))

        login_user(user)

        if not user.is_confirmed:

            token = generate_token(user.email)

            confirm_url = url_for(
                "user.confirm_email", token=token, _external=True
            )  # external=True to get the full url
            html = render_template("auth/confirmEmail.html", confirm_url=confirm_url)
            subject = "Please confirm your email"
            send_mail(user.email, subject, html)

            flash("Please confirm your email first", "warning")
            return redirect(url_for("user.inactive"))

        flash("Successfully logged in", "success")
        return redirect(url_for("main.index"))

    return render_template("auth/signIn.html", form=form)


@user.route("/confirm/<token>")
def confirm_email(token):

    email = confirm_token(token, expiration=180)  # 3 minutes

    if not email:
        flash("The confirmation link is invalid or expired", "error")
        return redirect(url_for("main.landing"))

    user = User.query.filter(User.email == email).first()

    if not user:
        flash("The confirmation link is invalid or expired", "error")
        return redirect(url_for("main.landing"))

    if user.is_confirmed:
        flash("Account already confirmed", "info")
        return redirect(url_for("main.community_guidelines"))

    user.is_confirmed = True
    user.updated_at = db.func.now()

    db.session.commit()

    login_user(user)

    flash("Account confirmed", "success")

    return redirect(url_for("main.community_guidelines"))


@user.route("/inactive")
@login_required
def inactive():

    user = User.query.filter(User.email == current_user.email).first()

    if user.is_confirmed:
        return redirect(url_for("main.index"))
    return render_template("auth/inactive.html")


@user.route("/resend")
@login_required
def resend_confirmation():
    user = User.query.filter(User.email == current_user.email).first()

    if user.is_confirmed:
        flash("Account already confirmed", "success")
        return redirect(url_for("main.index"))

    token = generate_token(user.email)
    confirm_url = url_for(
        "user.confirm_email", token=token, _external=True
    )  # external=True to get the full url
    html = render_template("auth/confirmEmail.html", confirm_url=confirm_url)
    subject = "Please confirm your email"
    send_mail(user.email, subject, html)

    flash("A new confirmation email has been sent via email", "success")

    return redirect(url_for("user.inactive"))


@user.route("/forgot-password", methods=["GET", "POST"])
@logout_required
def forgot_password():
    form = ForgotPasswordForm(request.form)

    if form.validate_on_submit():
        user = User.query.filter(User.email == form.email.data).first()

        if not user:
            flash("Email not found", "error")
            return redirect(url_for("user.forgot_password"))

        token = generate_token(user.email)
        reset_url = url_for(
            "user.reset_password", token=token, _external=True
        )  # external=True to get the full url
        html = render_template("auth/confirmResetPassword.html", reset_url=reset_url)
        subject = "Reset your password"
        send_mail(user.email, subject, html)

        flash("A password reset link has been sent via email", "success")

        return redirect(url_for("user.sign_in"))

    return render_template("auth/forgotPassword.html", form=form)


@user.route("/reset-password/<token>", methods=["GET", "POST"])
@logout_required
def reset_password(token):
    email = confirm_token(token, expiration=180)  # 3 minutes

    if not email:
        flash("The reset password link is invalid or expired", "error")
        return redirect(url_for("main.landing"))

    user = User.query.filter(User.email == email).first()

    if not user:
        flash("The reset password link is invalid or expired", "error")
        return redirect(url_for("main.landing"))

    form = ResetPasswordForm(request.form)

    if form.validate_on_submit():
        user.password = bcrypt.generate_password_hash(form.password.data).decode(
            "utf-8"
        )
        user.updated_at = db.func.now()

        db.session.commit()

        flash("Password reset successfully", "success")
        return redirect(url_for("user.sign_in"))

    return render_template("auth/resetPassword.html", form=form)


# Microsoft OAuth (Archived)
# @user.route("/sign-up/microsoft")
# @logout_required
# def microsoft_login():

#     microsoft_client = oauth.create_client("microsoft")
#     redirect_uri = None

#     if os.getenv("ENV") == "development" or os.getenv("DEBUG") == "True":
#         redirect_uri = url_for("user.microsoft_auth", _external=True)
#     elif os.getenv("ENV") == "production":
#         redirect_uri = url_for("user.microsoft_auth", _external=True, _scheme="https")
#     else:
#         raise Exception("Invalid Environment")

#     return microsoft_client.authorize_redirect(redirect_uri)


# @user.route("/sign-up/microsoft/callback")
# @logout_required
# def microsoft_auth():
#     microsoft_client = oauth.create_client("microsoft")
#     token = microsoft_client.authorize_access_token()

#     resp = microsoft_client.get("me")
#     user_info = resp.json()

#     user = User.query.filter_by(email=user_info["mail"]).first()

#     avatar_endpoint = (
#         f"https://graph.microsoft.com/v1.0/users/{user_info['id']}/photo/$value"
#     )

#     avatar_response = microsoft_client.get(avatar_endpoint)

#     avatar_url = None

#     if avatar_response.status_code == 200:
#         avatar_url = avatar_endpoint

#     if user:
#         login_user(user)

#         # when the user sign up for the first time, the user.anon_no is None
#         if user.anon_no is None:
#             return redirect(url_for("main.community_guidelines"))

#         flash("Successfully logged in", "success")
#         return redirect(url_for("main.index"))
#     else:
#         # check user email endwith mmu.edu.my
#         if not user_info["mail"].endswith("mmu.edu.my"):
#             flash("Please use your MMU email to sign up", "warning")
#             return redirect(url_for("main.landing"))

#         user = User(
#             {
#                 "email": user_info["mail"],
#                 "password": user_info["mail"],
#                 "username": user_info["displayName"],
#                 "avatar_url": avatar_url,
#                 "created_at": datetime.now(),
#             }
#         )
#         db.session.add(user)
#         db.session.commit()
#         login_user(user)
#         flash("Account created successfully", "success")
#         return redirect(url_for("main.community_guidelines"))


@user.route("/sign-out")
@login_required
def logout():
    logout_user()
    return redirect(url_for("main.landing"))


@user.route("/faked-user-login", methods=["GET", "POST"])
@logout_required
# @development_only
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
