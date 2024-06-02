from flask import Blueprint

faq = Blueprint("faq", __name__)

from . import views
