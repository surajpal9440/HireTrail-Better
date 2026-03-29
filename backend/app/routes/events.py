"""
Server-Sent Events endpoint.

EventSource (browser API) cannot send custom headers.
JWT is accepted via ?token= query param (configured in config.py via JWT_TOKEN_LOCATION).
"""
import json
import logging
from queue import Empty
from flask import Blueprint, Response, current_app
from flask_jwt_extended import jwt_required, get_jwt_identity

from app.services import sse_service

logger = logging.getLogger(__name__)

events_bp = Blueprint("events", __name__, url_prefix="/api/events")


@events_bp.route("/stream")
@jwt_required()
def stream():
    user_id = get_jwt_identity()
    q = sse_service.subscribe(user_id)

    def generate():
        try:
            while True:
                try:
                    payload = q.get(timeout=25)
                    yield sse_service.format_event(payload)
                except Empty:
                    # Heartbeat keeps the connection open through proxies/load-balancers
                    yield sse_service.heartbeat()
        except GeneratorExit:
            pass
        finally:
            sse_service.unsubscribe(user_id, q)

    return Response(
        generate(),
        mimetype="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "X-Accel-Buffering": "no",   # Disable nginx buffering
            "Connection": "keep-alive",
        },
    )
