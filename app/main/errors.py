from flask import render_template

from . import main


# status code 401 - unauthorized
@main.errorhandler(401)
def unauthorized_page(error):
    return render_template("errors/401.html"), 401


# status code 403 - forbidden
def forbidden(error):
    return render_template("errors/403.html"), 403


# status code 404 - not found
@main.errorhandler(404)
def page_not_found(error):
    return render_template("errors/404.html"), 404


# status code 500 - internal server error
@main.errorhandler(500)
def server_error_page(error):
    return render_template("errors/500.html"), 500
