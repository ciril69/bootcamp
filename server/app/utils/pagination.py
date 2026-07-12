import math
from typing import Any, List
from app.schemas.pagination import PaginationResponse

def get_pagination_params(page: int, limit: int) -> tuple[int, int]:
    """
    Get offset and limit values from page and limit parameters.
    """
    page = max(1, page)
    limit = max(1, limit)
    offset = (page - 1) * limit
    return offset, limit

def format_pagination(items: List[Any], total: int, page: int, limit: int) -> PaginationResponse:
    """
    Format data items and pagination metadata into a standard PaginationResponse.
    """
    pages = math.ceil(total / limit) if limit > 0 else 0
    return PaginationResponse(
        items=items,
        total=total,
        page=page,
        limit=limit,
        pages=pages,
    )
