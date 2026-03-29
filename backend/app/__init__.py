import logging
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from flask_bcrypt import Bcrypt
from flask_mail import Mail

db = SQLAlchemy()
jwt = JWTManager()
bcrypt = Bcrypt()
mail = Mail()

logger = logging.getLogger(__name__)


def create_app(config_name="development"):
    app = Flask(__name__)

    from app.config import config_map
    app.config.from_object(config_map[config_name])

    # Extensions
    db.init_app(app)
    jwt.init_app(app)
    bcrypt.init_app(app)
    mail.init_app(app)
    CORS(app, resources={r"/*": {"origins": "*"}})

    # JWT error handlers
    @jwt.unauthorized_loader
    def unauthorized_callback(reason):
        from app.utils import response as resp
        return resp.error("Authentication required", status_code=401)

    @jwt.invalid_token_loader
    def invalid_token_callback(reason):
        from app.utils import response as resp
        return resp.error("Invalid or expired token. Please log in again.", status_code=401)

    @jwt.expired_token_loader
    def expired_token_callback(jwt_header, jwt_payload):
        from app.utils import response as resp
        return resp.error("Your session has expired. Please log in again.", status_code=401)

    # Routes
    from app.routes import register_routes
    register_routes(app)

    # Database
    with app.app_context():
        db.create_all()
        # Enable WAL mode for SQLite to prevent 'database is locked' errors during SSE
        if app.config.get("SQLALCHEMY_DATABASE_URI", "").startswith("sqlite:"):
            from sqlalchemy import text
            db.session.execute(text("PRAGMA journal_mode=WAL;"))
            db.session.commit()

    # Scheduler (skip during testing)
    if config_name != "testing":
        _start_scheduler(app)

    return app


def _start_scheduler(app):
    """Start APScheduler with the daily reminder job."""
    try:
        from apscheduler.schedulers.background import BackgroundScheduler
        from apscheduler.triggers.cron import CronTrigger
        from app.services.reminder_service import send_reminder_emails

        scheduler = BackgroundScheduler(daemon=True)
        scheduler.add_job(
            func=send_reminder_emails,
            args=[app],
            trigger=CronTrigger(hour=9, minute=0),  # every day at 9am
            id="daily_reminders",
            replace_existing=True,
        )
        scheduler.start()
        logger.info("APScheduler started — daily reminders at 09:00")
    except Exception as e:
        logger.error(f"Failed to start scheduler: {e}")
