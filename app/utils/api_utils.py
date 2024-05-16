from flask import jsonify


def error_message(message, status_code):
    return (jsonify({"error": message, "status": status_code}), status_code)
