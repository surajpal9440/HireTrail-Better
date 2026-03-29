import logging
from flask import Blueprint
from flask_jwt_extended import jwt_required, get_jwt_identity
from marshmallow import ValidationError

from app.schemas.auth_schema import RegisterSchema, LoginSchema
from app.services import auth_service
from app.services.auth_service import AuthError
from app.utils import response as resp

logger = logging.getLogger(__name__)

auth_bp = Blueprint("auth", __name__, url_prefix="/api/auth")

register_schema = RegisterSchema()
login_schema = LoginSchema()


@auth_bp.route("/register", methods=["POST"])
def register():
    from flask import request
    json_data = request.get_json()
    if not json_data:
        return resp.error("Request body must be JSON", status_code=400)
    try:
        data = register_schema.load(json_data)
    except ValidationError as e:
        return resp.error("Validation failed", details=e.messages, status_code=422)

    try:
        user = auth_service.register_user(data)
    except AuthError as e:
        return resp.error(str(e), status_code=409)

    # Auto-login after register
    _, token = auth_service.login_user({"email": data["email"], "password": data["password"]})
    return resp.success(
        data={"user": user.to_dict(), "token": token},
        message="Account created successfully",
        status_code=201,
    )


@auth_bp.route("/login", methods=["POST"])
def login():
    from flask import request
    json_data = request.get_json()
    if not json_data:
        return resp.error("Request body must be JSON", status_code=400)
    try:
        data = login_schema.load(json_data)
    except ValidationError as e:
        return resp.error("Validation failed", details=e.messages, status_code=422)

    try:
        user, token = auth_service.login_user(data)
    except AuthError as e:
        return resp.error(str(e), status_code=401)

    return resp.success(
        data={"user": user.to_dict(), "token": token},
        message="Logged in successfully",
    )


@auth_bp.route("/me", methods=["GET"])
@jwt_required()
def me():
    user_id = get_jwt_identity()
    user = auth_service.get_user_by_id(user_id)
    if not user:
        return resp.error("User not found", status_code=404)
    return resp.success(data=user.to_dict())


@auth_bp.route("/logout", methods=["POST"])
@jwt_required()
def logout():
    # JWT is stateless — actual logout is handled client-side by deleting the token.
    # Server-side token blacklisting can be added later if needed.
    return resp.success(message="Logged out successfully")
