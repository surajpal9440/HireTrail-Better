from app.utils import response as resp


def not_found_handler(e):
    return resp.error("Resource not found", status_code=404)


def method_not_allowed_handler(e):
    return resp.error("Method not allowed", status_code=405)


def internal_error_handler(e):
    return resp.error("Internal server error", status_code=500)
