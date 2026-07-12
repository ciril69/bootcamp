"""
Rate Limiting Middleware
------------------------
Simple in-memory sliding-window rate limiter for write-heavy endpoints.

Protected paths (POST / PATCH / DELETE):
  /api/v1/cart
  /api/v1/orders
  /api/v1/contact

Limits (per client IP):
  - /api/v1/contact  → 5 requests / 60 seconds
  - /api/v1/orders   → 10 requests / 60 seconds
  - /api/v1/cart     → 60 requests / 60 seconds  (add / update / remove)

In production replace this with a Redis-backed limiter or API-gateway rules.
"""
import time
from collections import defaultdict, deque
from typing import Callable, Deque, Dict, Tuple

from fastapi import FastAPI, Request, Response, status
from fastapi.responses import JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware

# (max_requests, window_seconds)
_LIMITS: Dict[str, Tuple[int, int]] = {
    "/api/v1/contact": (5, 60),
    "/api/v1/orders": (10, 60),
    "/api/v1/cart": (60, 60),
}

# Write methods that should be rate-limited
_WRITE_METHODS = frozenset({"POST", "PATCH", "DELETE", "PUT"})

# In-memory store: {(path_prefix, client_ip): deque[request_timestamps]}
_store: Dict[Tuple[str, str], Deque[float]] = defaultdict(deque)


def _get_prefix(path: str) -> str | None:
    """Return the rate-limit bucket for the given path, or None if not limited."""
    for prefix in _LIMITS:
        if path == prefix or path.startswith(prefix + "/"):
            return prefix
    return None


class RateLimitMiddleware(BaseHTTPMiddleware):
    """ASGI middleware enforcing per-IP rate limits on write endpoints."""

    async def dispatch(self, request: Request, call_next: Callable) -> Response:
        if request.method not in _WRITE_METHODS:
            return await call_next(request)

        prefix = _get_prefix(request.url.path)
        if prefix is None:
            return await call_next(request)

        max_req, window = _LIMITS[prefix]
        client_ip = (
            request.client.host if request.client else "unknown"
        )
        key = (prefix, client_ip)
        now = time.monotonic()

        bucket = _store[key]
        # Evict timestamps outside the current window
        while bucket and bucket[0] < now - window:
            bucket.popleft()

        if len(bucket) >= max_req:
            retry_after = int(window - (now - bucket[0])) + 1
            return JSONResponse(
                status_code=status.HTTP_429_TOO_MANY_REQUESTS,
                headers={"Retry-After": str(retry_after)},
                content={
                    "success": False,
                    "error": {
                        "code": "RATE_LIMIT_EXCEEDED",
                        "message": (
                            f"Too many requests. "
                            f"Limit: {max_req} per {window}s. "
                            f"Retry after {retry_after}s."
                        ),
                    },
                },
            )

        bucket.append(now)
        return await call_next(request)


def setup_rate_limiting(app: FastAPI) -> None:
    """Register the rate-limiting middleware on the app."""
    app.add_middleware(RateLimitMiddleware)
