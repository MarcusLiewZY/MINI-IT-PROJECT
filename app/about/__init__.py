from flask import Blueprint

about = Blueprint("ABOUT", __name__)

from . import views
