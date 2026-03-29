from flask import jsonify


def success(data=None, message="", status_code=200):
    response = {"success": True, "message": message}
    if data is not None:
        response["data"] = data
    return jsonify(response), status_code


def error(message="Something went wrong", details=None, status_code=400):
    response = {"success": False, "error": message}
    if details is not None:
        response["details"] = details
    return jsonify(response), status_code
