"""
Server-Sent Events (SSE) service.

Each authenticated user can have multiple browser tabs connected.
When a job is created/updated/deleted, we publish to all of that user's queues.
The SSE route reads from the queue and streams events to the browser.
"""
import json
import logging
from queue import Queue, Empty
from threading import Lock
from collections import defaultdict

logger = logging.getLogger(__name__)

# user_id (str) → list of Queue objects (one per connected tab)
_listeners: dict[str, list[Queue]] = defaultdict(list)
_lock = Lock()


def subscribe(user_id: str) -> Queue:
    """Register a new SSE listener for a user. Returns the queue to read from."""
    q = Queue(maxsize=50)
    with _lock:
        _listeners[user_id].append(q)
    logger.debug(f"SSE: user {user_id} connected ({len(_listeners[user_id])} tabs)")
    return q


def unsubscribe(user_id: str, q: Queue):
    """Remove a listener when the client disconnects."""
    with _lock:
        if q in _listeners[user_id]:
            _listeners[user_id].remove(q)
        if not _listeners[user_id]:
            del _listeners[user_id]
    logger.debug(f"SSE: user {user_id} disconnected")


def publish(user_id: str, event_type: str, data: dict):
    """Push an event to all connected tabs for a user."""
    payload = {"type": event_type, "data": data}
    with _lock:
        listeners = list(_listeners.get(str(user_id), []))

    dropped = 0
    for q in listeners:
        try:
            q.put_nowait(payload)
        except Exception:
            dropped += 1

    if listeners:
        logger.debug(f"SSE: published '{event_type}' to user {user_id} ({len(listeners)} tabs, {dropped} dropped)")


def format_event(payload: dict) -> str:
    """Format a dict as an SSE message string."""
    return f"data: {json.dumps(payload)}\n\n"


def heartbeat() -> str:
    """SSE comment used as a keep-alive ping."""
    return ": ping\n\n"
