from flask import render_template

from app import app
from flask_login import current_user


# status code 401 - unauthorized
@app.errorhandler(401)
def unauthorized_page(error):
    return render_template("errors/401.html"), 401


# status code 403 - forbidden
def forbidden(error):
    return render_template("errors/403.html"), 403


# status code 404 - not found
@app.errorhandler(404)
def page_not_found(error):
    return render_template("errors/404.html", user=current_user), 404


# status code 500 - internal server error
@app.errorhandler(500)
def server_error_page(error):
    return render_template("errors/500.html"), 500
