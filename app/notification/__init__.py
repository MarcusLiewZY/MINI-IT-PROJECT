from flask import Blueprint

notification = Blueprint("notification", __name__)

from . import views
