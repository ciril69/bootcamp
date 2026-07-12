"""
Products Router
--------------
GET  /products             – Paginated list with filters & sort
GET  /products/featured    – Featured homepage products
GET  /products/{slug}      – Full product detail (404 if missing)

IMPORTANT: /featured must be registered BEFORE /{slug} so FastAPI doesn't
           treat the literal string "featured" as a slug parameter.
"""
from typing import Optional

from fastapi import APIRouter, Query, status
from fastapi.responses import JSONResponse

from app.schemas.pagination import PaginationResponse
from app.services.product import ProductService
from app.utils.response import format_success_response
from app.constants import DEFAULT_PAGE, DEFAULT_LIMIT

router = APIRouter(prefix="/products", tags=["Products"])
_svc = ProductService()


@router.get(
    "/featured",
    summary="Get Featured Products",
    description="Returns featured products displayed on the homepage.",
    status_code=status.HTTP_200_OK,
    responses={
        200: {"description": "Featured products returned successfully"},
    },
)
async def get_featured_products(
    limit: int = Query(default=8, ge=1, le=50, description="Maximum number of featured products"),
) -> dict:
    """Return featured products for the homepage."""
    items = _svc.get_featured_products(limit=limit)
    return format_success_response(data=items)


@router.get(
    "",
    summary="List Products",
    description=(
        "Return a paginated list of products. "
        "Supports filtering by category slug, search, featured flag, price range, "
        "and sorting (newest, price_asc, price_desc)."
    ),
    status_code=status.HTTP_200_OK,
    responses={
        200: {"description": "Products returned successfully"},
    },
)
async def list_products(
    category: Optional[str] = Query(default=None, description="Filter by category slug"),
    search: Optional[str] = Query(default=None, description="Full-text search by product name"),
    featured: Optional[bool] = Query(default=None, description="Filter featured products"),
    min_price: Optional[float] = Query(default=None, ge=0, description="Minimum price filter"),
    max_price: Optional[float] = Query(default=None, ge=0, description="Maximum price filter"),
    sort: Optional[str] = Query(
        default=None,
        description="Sort order: newest (default), price_asc, price_desc",
        pattern="^(newest|price_asc|price_desc)$",
    ),
    page: int = Query(default=DEFAULT_PAGE, ge=1, description="Page number"),
    limit: int = Query(default=DEFAULT_LIMIT, ge=1, le=100, description="Items per page"),
) -> dict:
    """Return a paginated, filtered, sorted list of products."""
    pagination: PaginationResponse = _svc.list_products(
        category=category,
        search=search,
        featured=featured,
        min_price=min_price,
        max_price=max_price,
        sort=sort,
        page=page,
        limit=limit,
    )
    return {
        "success": True,
        "data": pagination.items,
        "pagination": {
            "total": pagination.total,
            "page": pagination.page,
            "limit": pagination.limit,
            "pages": pagination.pages,
        },
    }


@router.get(
    "/{slug}",
    summary="Get Product by Slug",
    description=(
        "Return full product details including image gallery, category, "
        "related products, and customization availability. "
        "Returns 404 if the product is not found."
    ),
    status_code=status.HTTP_200_OK,
    responses={
        200: {"description": "Product found and returned"},
        404: {"description": "Product not found"},
    },
)
async def get_product(slug: str) -> dict:
    """Return a single product's full details by slug."""
    product = _svc.get_product(slug)
    return format_success_response(data=product)
