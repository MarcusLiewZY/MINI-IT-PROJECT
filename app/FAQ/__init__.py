from flask import Blueprint

faq = Blueprint("FAQ", __name__)

from . import views
