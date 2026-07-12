"""
Request Logging Middleware
--------------------------
Logs every incoming HTTP request and its response status/duration.

Deliberately omits PII fields: address, phone, email, and request bodies
for write endpoints that carry customer data.
"""
import time
from typing import Callable

from fastapi import FastAPI, Request, Response
from loguru import logger
from starlette.middleware.base import BaseHTTPMiddleware

# Fields that must never appear in logs (PII / sensitive)
_SENSITIVE_QUERY_PARAMS = frozenset({"email", "phone", "address"})


class RequestLoggingMiddleware(BaseHTTPMiddleware):
    """ASGI middleware that logs each request/response pair."""

    async def dispatch(self, request: Request, call_next: Callable) -> Response:
        start = time.perf_counter()

        # Build a sanitised query-string (drop PII keys)
        safe_params = {
            k: v
            for k, v in request.query_params.items()
            if k.lower() not in _SENSITIVE_QUERY_PARAMS
        }
        qs = f"?{'&'.join(f'{k}={v}' for k, v in safe_params.items())}" if safe_params else ""

        logger.info(
            f"→ {request.method} {request.url.path}{qs} "
            f"client={request.client.host if request.client else 'unknown'}"
        )

        try:
            response: Response = await call_next(request)
        except Exception:
            logger.exception(
                f"Unhandled exception in {request.method} {request.url.path}"
            )
            raise

        elapsed_ms = (time.perf_counter() - start) * 1000
        level = "INFO" if response.status_code < 400 else "WARNING"
        logger.log(
            level,
            f"← {response.status_code} {request.method} {request.url.path} "
            f"({elapsed_ms:.1f} ms)",
        )

        return response


def setup_request_logging(app: FastAPI) -> None:
    """Register the request-logging middleware on the app."""
    app.add_middleware(RequestLoggingMiddleware)
