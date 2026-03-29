from app.routes.auth import auth_bp
from app.routes.jobs import jobs_bp
from app.routes.events import events_bp
from app.utils.errors import not_found_handler, method_not_allowed_handler, internal_error_handler


def register_routes(app):
    app.register_blueprint(auth_bp)
    app.register_blueprint(jobs_bp)
    app.register_blueprint(events_bp)

    app.register_error_handler(404, not_found_handler)
    app.register_error_handler(405, method_not_allowed_handler)
    app.register_error_handler(500, internal_error_handler)
