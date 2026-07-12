"""
Health Router – GET /health
Returns server health status.
"""
from fastapi import APIRouter
from app.schemas.health import HealthResponse

router = APIRouter(prefix="/health", tags=["Health"])


@router.get(
    "",
    response_model=HealthResponse,
    summary="Health Check",
    description="Returns the current health status of the API server.",
    responses={
        200: {"description": "Server is healthy"},
    },
)
async def get_health() -> HealthResponse:
    return HealthResponse(status="healthy")
