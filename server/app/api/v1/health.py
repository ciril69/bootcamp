from fastapi import APIRouter

router = APIRouter(prefix="/health", tags=["Health"])

@router.get("", response_model=dict)
async def get_health() -> dict[str, str]:
    """
    Health check endpoint to verify server status.
    """
    return {"status": "healthy"}
