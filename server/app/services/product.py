from typing import List, Optional
from loguru import logger
from app.repositories.product import ProductRepository
from app.exceptions import ProductNotFound
from app.utils.pagination import get_pagination_params, format_pagination
from app.schemas.pagination import PaginationResponse
from app.constants import DEFAULT_PAGE, DEFAULT_LIMIT


class ProductService:
    """
    Service class for Product business logic.
    Handles filtering, searching, pagination, and error raising.
    """

    def __init__(self, product_repo: Optional[ProductRepository] = None) -> None:
        self.product_repo = product_repo or ProductRepository()

    def list_products(
        self,
        *,
        category: Optional[str] = None,
        search: Optional[str] = None,
        featured: Optional[bool] = None,
        min_price: Optional[float] = None,
        max_price: Optional[float] = None,
        sort: Optional[str] = None,
        page: int = DEFAULT_PAGE,
        limit: int = DEFAULT_LIMIT,
    ) -> PaginationResponse:
        """
        Return a paginated list of products with optional filters and sorting.
        """
        logger.debug(
            f"Listing products: category={category} search={search} "
            f"featured={featured} sort={sort} page={page} limit={limit}"
        )
        offset, limit = get_pagination_params(page, limit)
        items, total = self.product_repo.list_products(
            category_slug=category,
            search=search,
            featured=featured,
            min_price=min_price,
            max_price=max_price,
            sort=sort,
            offset=offset,
            limit=limit,
        )
        return format_pagination(items, total, page, limit)

    def get_product(self, slug: str) -> dict:
        """
        Return full product details by slug with related products.
        Raises ProductNotFound if not found.
        """
        logger.debug(f"Fetching product by slug: {slug}")
        product = self.product_repo.find_by_slug(slug)
        if not product:
            raise ProductNotFound(f"Product with slug '{slug}' not found.")

        # Attach related products
        related = self.product_repo.get_related(
            product_id=product["id"],
            category_id=product["category_id"],
            limit=4,
        )
        product["related_products"] = related
        return product

    def get_featured_products(self, limit: int = 8) -> List[dict]:
        """
        Return a list of featured products for the homepage.
        """
        logger.debug("Fetching featured products")
        return self.product_repo.get_featured(limit=limit)
