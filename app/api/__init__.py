from flask import Blueprint, jsonify

api = Blueprint("api", __name__, url_prefix="/api")

from . import tag, user, post, comment, pagination
