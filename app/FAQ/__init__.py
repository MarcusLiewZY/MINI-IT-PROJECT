from flask import Blueprint

FAQ_bp = Blueprint("FAQ", __name__)

from . import views
