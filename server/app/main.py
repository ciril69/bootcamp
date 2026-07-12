from contextlib import asynccontextmanager
from typing import AsyncGenerator
from fastapi import FastAPI
from loguru import logger

from app.config import get_settings
from app.core import setup_logging
from app.middleware import setup_cors
from app.exceptions import setup_exception_handlers
from app.api import v1_router

# Setup centralized logging before app initialization
setup_logging()

@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
    # Startup event
    logger.info(f"Starting up {app.title}...")
    logger.info(f"Environment: {get_settings().APP_ENV}")
    logger.info(f"Debug mode: {get_settings().DEBUG}")
    
    yield
    
    # Shutdown event
    logger.info(f"Shutting down {app.title}...")

settings = get_settings()

app = FastAPI(
    title=settings.APP_NAME,
    version="1.0.0",
    description="Backend API for Streetwear E-Commerce Demo Website",
    debug=settings.DEBUG,
    openapi_url=f"{settings.API_PREFIX}/openapi.json" if settings.DEBUG else None,
    docs_url="/docs" if settings.DEBUG else None,
    redoc_url="/redoc" if settings.DEBUG else None,
    lifespan=lifespan,
)

# Setup CORS middleware
setup_cors(app, settings)

# Setup Global Exception Handlers
setup_exception_handlers(app)

# Register Routers
app.include_router(v1_router, prefix=settings.API_PREFIX)

# Expose a root health check endpoint as well for convenience
@app.get("/health", tags=["Health"], response_model=dict[str, str])
async def root_health() -> dict[str, str]:
    """
    Root health check endpoint.
    """
    return {"status": "healthy"}
