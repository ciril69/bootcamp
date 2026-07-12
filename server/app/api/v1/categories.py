"""
Categories Router
-----------------
GET /categories – Return all clothing categories.
"""
from fastapi import APIRouter, status

from app.services.category import CategoryService
from app.utils.response import format_success_response

router = APIRouter(prefix="/categories", tags=["Categories"])
_svc = CategoryService()


@router.get(
    "",
    summary="List Categories",
    description="Returns all clothing categories available in the store.",
    status_code=status.HTTP_200_OK,
    responses={
        200: {"description": "Categories returned successfully"},
    },
)
async def list_categories() -> dict:
    """Return all categories."""
    categories = _svc.get_all_categories()
    return format_success_response(data=categories)
