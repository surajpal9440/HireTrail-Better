import logging
from flask_jwt_extended import create_access_token
from app import db, bcrypt
from app.models.user import User

logger = logging.getLogger(__name__)


class AuthError(Exception):
    """Raised for known authentication failures."""
    pass


def register_user(data):
    email = data["email"].lower().strip()

    if User.query.filter_by(email=email).first():
        raise AuthError("An account with this email already exists.")

    password_hash = bcrypt.generate_password_hash(data["password"]).decode("utf-8")
    user = User(
        name=data["name"].strip(),
        email=email,
        password_hash=password_hash,
    )
    db.session.add(user)
    db.session.commit()
    logger.info(f"New user registered: {email} (id={user.id})")
    return user


def login_user(data):
    email = data["email"].lower().strip()
    user = User.query.filter_by(email=email).first()

    if not user or not bcrypt.check_password_hash(user.password_hash, data["password"]):
        raise AuthError("Invalid email or password.")

    token = create_access_token(identity=str(user.id))
    logger.info(f"User logged in: {email}")
    return user, token


def get_user_by_id(user_id):
    return User.query.get(int(user_id))
