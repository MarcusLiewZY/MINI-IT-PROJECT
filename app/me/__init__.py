from flask import Blueprint

me_bp = Blueprint("me", __name__, url_prefix="/me")

from . import views
