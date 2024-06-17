from uuid import UUID
from datetime import datetime
from flask import jsonify, request
from http import HTTPStatus as responseStatus


from . import api
from app import db
from app.models.tag import Tag
from app.utils.api_utils import error_message
from app.utils.decorators import api_login_required


@api.route("/tags", methods=["GET"])
@api_login_required
def get_tags():
    """
    Get all tag-name and tag-color pairs.
    Returns:
        A JSON object where the keys are tag names and the values are tag colors,
        and an HTTP status code.
    """
    try:
        tags = Tag.query.all()

        tags_dict = {}

        for tag in tags:
            tags_dict[tag.name] = tag.color

        return (
            jsonify(
                {
                    "status": responseStatus.OK,
                    "message": "Tags retrieved successfully",
                    "tags": tags_dict,
                },
            ),
            responseStatus.OK,
        )
    except Exception as e:
        print(e)
        return error_message(
            "Internal Server Error", responseStatus.INTERNAL_SERVER_ERROR
        )


@api.route("/tags", methods=["POST"])
@api_login_required
def create_tag():
    """
    Create a new tag.
    Args:
        name: The name of the tag.
        color: The color of the tag.
        description: The description of the tag.
    Returns:
        A JSON object with the new tag's name, color, and description, and an HTTP status code.
    """
    try:
        data = request.json
        name = data.get("name")

        if Tag.query.filter(Tag.name == name).first():
            return error_message("Tag already exists", responseStatus.CONFLICT)

        tag = Tag(
            {
                "name": name,
                "color": data.get("color"),
                "description": data.get("description"),
                "created_at": datetime.now(),
            }
        )

        db.session.add(tag)
        db.session.commit()

        return (
            jsonify(
                {
                    "status": responseStatus.CREATED,
                    "message": "Tag created successfully",
                    "tag": {
                        "id": tag.id,
                        "name": tag.name,
                        "color": tag.color,
                        "description": tag.description,
                    },
                }
            ),
            responseStatus.CREATED,
        )

    except Exception as e:
        db.session.rollback()
        print(e)
        return error_message(
            "Internal Server Error", responseStatus.INTERNAL_SERVER_ERROR
        )


@api.route("/tags/<tag_id>", methods=["GET"])
@api_login_required
def get_tag(tag_id):
    """
    Get a tag by its id.
    Args:
        tag_id: The id of the tag.
    Return:
        A JSON object with the tag name, color, and description, and an HTTP status code.
    """
    try:
        print(tag_id)
        print(type(tag_id))
        tag = Tag.query.filter(Tag.id == UUID(tag_id)).first()

        if tag is None:
            return error_message("Tag not found", responseStatus.NOT_FOUND)

        return (
            jsonify(
                {
                    "status": responseStatus.OK,
                    "message": "Tag retrieved successfully",
                    "tag": {
                        "name": tag.name,
                        "color": tag.color,
                        "description": tag.description,
                    },
                }
            ),
            responseStatus.OK,
        )

    except Exception as e:
        print(e)
        return error_message(
            "Internal Server Error", responseStatus.INTERNAL_SERVER_ERROR
        )


@api.route("/tags/<tag_id>", methods=["PUT"])
@api_login_required
def edit_tag(tag_id):
    """
    Edit a tag by its id.
    Args:
        tag_id: The id of the tag.
        tag_name: The name of the tag.
        tag_color: The color of the tag.
        tag_description: The description of the tag.
    Returns:
        A JSON object with the updated tag's name, color, and description, and an HTTP status code.
    """
    try:
        data = request.json

        tag = Tag.query.filter(Tag.id == UUID(tag_id)).first()

        if tag is None:
            return error_message("Tag not found", responseStatus.NOT_FOUND)

        name = data.get("name")

        if Tag.query.filter(Tag.name == name).first() is not None:
            return error_message("Tag already exists", responseStatus.CONFLICT)

        tag.name = name
        tag.color = data.get("color")
        tag.description = data.get("description")
        tag.updated_at = datetime.now()

        db.session.commit()

        return (
            jsonify(
                {
                    "status": responseStatus.OK,
                    "message": "Tag updated successfully",
                    "tag": {
                        "id": tag.id,
                        "name": tag.name,
                        "color": tag.color,
                        "description": tag.description,
                    },
                }
            ),
            responseStatus.OK,
        )

    except Exception as e:
        db.session.rollback()
        print(e)
        return error_message(
            "Internal Serve Error", responseStatus.INTERNAL_SERVER_ERROR
        )


@api.route("/tags/<tag_id>", methods=["DELETE"])
@api_login_required
def delete_tag(tag_id):
    """
    Delete a tag by its id.
    Args:
        tag_id: The id of the tag.
    Returns:
        A JSON object with a message indicating the tag was deleted successfully, and an HTTP status code.
    """
    try:
        tag = Tag.query.filter(Tag.id == UUID(tag_id)).first()

        if tag is None:
            return error_message("Tag not found", responseStatus.NOT_FOUND)

        db.session.delete(tag)
        db.session.commit()

        return (
            jsonify(
                {
                    "status": responseStatus.OK,
                    "message": "Tag deleted successfully",
                    "tagId": tag.id,
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
