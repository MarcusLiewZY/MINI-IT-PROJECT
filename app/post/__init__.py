from flask import Blueprint

post = Blueprint("post", __name__, url_prefix="/posts")

from . import views
from . import forms
