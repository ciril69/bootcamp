"""
Application entry-point
-----------------------
Creates the FastAPI app, registers middleware, exception handlers, and routers.

/docs  and /redoc are always available (both in development and production)
so the frontend team and partners can always inspect the API contract.
"""
from contextlib import asynccontextmanager
from typing import AsyncGenerator

from fastapi import FastAPI
from loguru import logger

from app.config import get_settings
from app.core import setup_logging
from app.middleware import setup_cors, setup_request_logging, setup_rate_limiting
from app.exceptions import setup_exception_handlers
from app.api import v1_router

# Configure structured logging before anything else
setup_logging()


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
    logger.info(f"Starting up {app.title} …")
    logger.info(f"Environment : {get_settings().APP_ENV}")
    logger.info(f"Debug mode  : {get_settings().DEBUG}")
    logger.info(f"Docs        : /docs  |  /redoc")
    yield
    logger.info(f"Shutting down {app.title} …")


settings = get_settings()

app = FastAPI(
    title=settings.APP_NAME,
    version="1.0.0",
    description=(
        "Backend REST API for the MONOLITH Streetwear E-Commerce Demo. "
        "All endpoints are prefixed with /api/v1. "
        "No authentication required for Version 1."
    ),
    # /docs and /redoc are intentionally always exposed so the API contract is
    # always discoverable regardless of environment.
    openapi_url=f"{settings.API_PREFIX}/openapi.json",
    docs_url="/docs",
    redoc_url="/redoc",
    lifespan=lifespan,
)

# ── Middleware (order matters – outermost wraps first) ─────────────────────
# CORS must be outermost so pre-flight OPTIONS requests are handled before
# any other middleware inspects them.
setup_cors(app, settings)

# Rate limiting protects write endpoints from abuse.
setup_rate_limiting(app)

# Request logging captures every request + response pair for observability.
setup_request_logging(app)

# ── Exception handlers ─────────────────────────────────────────────────────
setup_exception_handlers(app)

# ── Routers ────────────────────────────────────────────────────────────────
app.include_router(v1_router, prefix=settings.API_PREFIX)


# ── Convenience root health check ─────────────────────────────────────────
@app.get(
    "/health",
    tags=["Health"],
    summary="Root Health Check",
    description="Quick liveness probe — also available at /api/v1/health.",
    response_model=dict,
)
async def root_health() -> dict:
    return {"status": "healthy"}
