import requests
from uuid import UUID
from datetime import datetime
from flask import jsonify, request
from flask_login import login_user, logout_user
from http import HTTPStatus as responseStatus

from . import api
from app import db
from app.models import User
from app.utils.helper import format_datetime
from app.utils.api_utils import error_message
from app.utils.decorators import api_login_required, api_logout_required, api_is_admin


@api.route("/accounts/sign-up/microsoft/callback", methods=["GET"])
@api_logout_required
def microsoft_auth():
    """
    Authenticate the user using Microsoft OAuth.
    Args:
        None
    Returns:
        A JSON object containing the user's record and an HTTP status code.
    """
    try:
        access_token = request.args.get("access_token")
        if not access_token:
            return error_message("Access token is missing", responseStatus.BAD_REQUEST)

        headers = {"Authorization": f"Bearer {access_token}"}

        # Fetch user information from Microsoft Graph API
        user_info_response = requests.get(
            "https://graph.microsoft.com/v1.0/me", headers=headers
        )
        user_info = user_info_response.json()

        if user_info_response.status_code != 200:
            return error_message(
                "Failed to fetch user information", responseStatus.UNAUTHORIZED
            )

        user = User.query.filter_by(email=user_info["mail"]).first()

        # Fetch user avatar
        avatar_endpoint = (
            f"https://graph.microsoft.com/v1.0/users/{user_info['id']}/photo/$value"
        )
        avatar_response = requests.get(avatar_endpoint, headers=headers)

        avatar_url = None

        if avatar_response.status_code == 200:
            avatar_url = avatar_endpoint

        if user:
            login_user(user)
            return (
                jsonify(
                    {
                        "status": responseStatus.OK,
                        "message": "Successfully logged in.",
                        "user_id": user.id,
                        "user_email": user.email,
                    }
                ),
                responseStatus.OK,
            )

        else:
            # Check if the user email ends with mmu.edu.my
            if not user_info["mail"].endswith("mmu.edu.my"):
                return error_message(
                    "Please use your MMU email to sign up", responseStatus.BAD_REQUEST
                )

            user = User(
                email=user_info["mail"],
                password=user_info["mail"],
                username=user_info["displayName"],
                avatar_url=avatar_url,
                created_at=format_datetime(datetime.now()),
            )
            db.session.add(user)
            db.session.commit()
            login_user(user)

            return jsonify(
                {
                    "status": responseStatus.OK,
                    "message": "Account created successfully",
                    "user_id": user.id,
                    "user_email": user.email,
                }
            )

    except Exception as e:
        print(e)
        return error_message(
            "Internal Server Error", responseStatus.INTERNAL_SERVER_ERROR
        )


@api.route("/accounts/sign-out", methods=["GET"])
@api_login_required
def logout():
    """
    Log out the current user.
    Args:
        None
    Returns:
        A JSON object containing a success message and an HTTP status code.
    """
    try:
        logout_user()
        return (
            jsonify(
                {"status": responseStatus.OK, "message": "Successfully logged out."}
            ),
            responseStatus.OK,
        )

    except Exception as e:
        print(e)
        return error_message(
            "Internal Server Error", responseStatus.INTERNAL_SERVER_ERROR
        )


@api.route("/accounts/faked-user-login", methods=["GET"])
@api_logout_required
def faked_user_login():
    """
    Log in as a fake user.
    Args:
        email: The email of the fake user.
    Returns:
        A JSON object containing the user id, email, success message and HTTP status code.
    """
    try:

        email = request.json.get("email")

        if email is None:
            return error_message(
                "Missing required parameter email", responseStatus.BAD_REQUEST
            )

        user = User.query.filter_by(email=email).first()

        if user is None:
            return error_message("User not found", responseStatus.NOT_FOUND)

        login_user(user)

        return (
            jsonify(
                {
                    "status": responseStatus.OK,
                    "message": "Successfully logged in.",
                    "user_id": user.id,
                    "user_email": user.email,
                }
            ),
            responseStatus.OK,
        )

    except Exception as e:
        print(e)
        return error_message(
            "Internal Server Error", responseStatus.INTERNAL_SERVER_ERROR
        )


@api.route("/accounts/<account_id>", methods=["DELETE"])
@api_login_required
@api_is_admin
def delete_account(account_id):
    """
    Delete an account by its ID permanently. This action is only allowed for admin users.
    Args:
        account_id: The ID of the account to delete.
    Returns:
        A JSON object containing a success message and an HTTP status code.
    """
    try:
        if account_id is None:
            return error_message("Account ID is required", responseStatus.BAD_REQUEST)

        user = User.query.get(UUID(account_id))

        if user is None:
            return error_message("Account not found", responseStatus.NOT_FOUND)

        db.session.delete(user)
        db.session.commit()

        return (
            jsonify(
                {
                    "status": responseStatus.OK,
                    "message": "Account deleted successfully.",
                }
            ),
            responseStatus.OK,
        )

    except Exception as e:
        db.session.rollback()
        print(e)
        return error_message(
            "Internal Server Error", responseStatus.INTERNAL_SERVER_ERROR
        )
