from flask import jsonify
from http import HTTPStatus as responseStatus

from . import api
from app.models.tag import Tag


@api.route("/tags", methods=["GET"])
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
        return jsonify(tags_dict), responseStatus.OK
    except Exception as e:
        print(e)
        return (
            jsonify({"error": "Internal Server Error"}),
            responseStatus.INTERNAL_SERVER_ERROR,
        )
