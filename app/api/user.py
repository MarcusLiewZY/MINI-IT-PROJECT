from uuid import UUID
from flask import jsonify, request
from http import HTTPStatus as responseStatus

from . import api
from app import db
from app.models.user import User


@api.route("/accounts/<account_id>", methods=["DELETE"])
def delete_account(account_id):
    """
    Delete an account by its ID permanently.
    Args:
        account_id: The ID of the account to delete.
    Returns:
        A JSON object containing the account's record and an HTTP status code.
    """
    try:
        if account_id is None:
            return (
                jsonify({"error": "Account ID is required."}),
                responseStatus.BAD_REQUEST,
            )

        user = User.query.get(UUID(account_id))

        if user is None:
            return (jsonify({"error": "Account not found."}), responseStatus.NOT_FOUND)

        db.session.delete(user)
        db.session.commit()

        return (
            jsonify({"message": "Account deleted successfully."}),
            responseStatus.OK,
        )

    except Exception as e:
        print(e)
        return (
            jsonify({"error": "Internal Server Error"}),
            responseStatus.INTERNAL_SERVER_ERROR,
        )
