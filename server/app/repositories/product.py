from typing import Any, List, Optional
from supabase import Client
from app.db.client import supabase as default_supabase


class ProductRepository:
    """
    Repository class for managing Products via Supabase.
    No business logic — only raw Supabase data access.
    """

    def __init__(self, db: Optional[Client] = None) -> None:
        self.db = db if db is not None else default_supabase

    def list_products(
        self,
        *,
        category_slug: Optional[str] = None,
        search: Optional[str] = None,
        featured: Optional[bool] = None,
        min_price: Optional[float] = None,
        max_price: Optional[float] = None,
        sort: Optional[str] = None,
        offset: int = 0,
        limit: int = 10,
    ) -> tuple[List[dict], int]:
        """
        List products with optional filters, search, sorting, and pagination.
        Returns (items, total_count).
        """
        query = (
            self.db.table("products")
            .select(
                "*, categories(id, name, slug), product_images(id, image_url, display_order)",
                count="exact",
            )
        )

        if category_slug:
            # Filter by category slug via join
            cat_resp = (
                self.db.table("categories").select("id").eq("slug", category_slug).execute()
            )
            if cat_resp.data:
                query = query.eq("category_id", cat_resp.data[0]["id"])
            else:
                return [], 0

        if search:
            query = query.ilike("name", f"%{search}%")

        if featured is not None:
            query = query.eq("featured", featured)

        if min_price is not None:
            query = query.gte("price", min_price)

        if max_price is not None:
            query = query.lte("price", max_price)

        # Sorting
        if sort == "price_asc":
            query = query.order("price", desc=False)
        elif sort == "price_desc":
            query = query.order("price", desc=True)
        else:
            # Default: newest first
            query = query.order("created_at", desc=True)

        query = query.range(offset, offset + limit - 1)

        response = query.execute()
        total = response.count if response.count is not None else len(response.data)
        return response.data, total

    def find_by_slug(self, slug: str) -> Optional[dict]:
        """
        Get full product details by slug, including images and category.
        """
        response = (
            self.db.table("products")
            .select(
                "*, categories(id, name, slug), product_images(id, image_url, display_order)"
            )
            .eq("slug", slug)
            .execute()
        )
        return response.data[0] if response.data else None

    def find_by_id(self, product_id: str) -> Optional[dict]:
        """
        Get a product by its UUID.
        """
        response = (
            self.db.table("products")
            .select(
                "*, categories(id, name, slug), product_images(id, image_url, display_order)"
            )
            .eq("id", product_id)
            .execute()
        )
        return response.data[0] if response.data else None

    def get_featured(self, limit: int = 8) -> List[dict]:
        """
        Get featured products for the homepage.
        """
        response = (
            self.db.table("products")
            .select(
                "*, categories(id, name, slug), product_images(id, image_url, display_order)"
            )
            .eq("featured", True)
            .order("created_at", desc=True)
            .limit(limit)
            .execute()
        )
        return response.data

    def get_related(self, product_id: str, category_id: str, limit: int = 4) -> List[dict]:
        """
        Get related products in the same category, excluding the current product.
        """
        response = (
            self.db.table("products")
            .select(
                "*, categories(id, name, slug), product_images(id, image_url, display_order)"
            )
            .eq("category_id", category_id)
            .neq("id", product_id)
            .order("created_at", desc=True)
            .limit(limit)
            .execute()
        )
        return response.data
