from flask import Blueprint

ABOUT_bp = Blueprint("ABOUT", __name__)

from . import views
