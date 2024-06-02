from functools import wraps
from http import HTTPStatus as responseStatus

from flask import redirect, url_for, flash
from flask_login import current_user
from .api_utils import error_message


def login_required(func):
    @wraps(func)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated:
            return redirect(url_for("main.landing"))
        return func(*args, **kwargs)

    return decorated_function


def logout_required(func):
    @wraps(func)
    def decorated_function(*args, **kwargs):
        if current_user.is_authenticated:
            return redirect(url_for("main.index"))
        return func(*args, **kwargs)

    return decorated_function


def is_admin(func):
    @wraps(func)
    def decorated_function(*args, **kwargs):
        if not current_user.is_admin:
            flash("You are not authorized to access this page", "warning")
            return redirect(url_for("main.index"))
        return func(*args, **kwargs)

    return decorated_function


def require_accept_community_guideline(func):
    @wraps(func)
    def decorated_function(*args, **kwargs):
        if current_user.anon_no is None:
            flash("Please accept the community guidelines first", "warning")
            return redirect(url_for("main.community_guidelines"))
        return func(*args, **kwargs)

    return decorated_function


# api decorators
def api_login_required(func):
    @wraps(func)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated:
            return error_message("Login required", responseStatus.UNAUTHORIZED)
        return func(*args, **kwargs)

    return decorated_function


def api_logout_required(func):
    @wraps(func)
    def decorated_function(*args, **kwargs):
        if current_user.is_authenticated:
            return error_message("Logout required", responseStatus.UNAUTHORIZED)
        return func(*args, **kwargs)

    return decorated_function


def api_is_admin(func):
    @wraps(func)
    def decorated_function(*args, **kwargs):
        if not current_user.is_admin:
            return error_message("Admin role is required", responseStatus.UNAUTHORIZED)
        return func(*args, **kwargs)

    return decorated_function
