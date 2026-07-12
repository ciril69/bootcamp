from typing import Any, Dict, List, Optional
from supabase import Client
from app.db.client import supabase as default_supabase


class CartRepository:
    """
    Repository class for managing Cart Items via Supabase.
    Anonymous carts are keyed by session_id.
    No business logic — only raw Supabase data access.
    """

    def __init__(self, db: Optional[Client] = None) -> None:
        self.db = db if db is not None else default_supabase

    def get_cart_items(self, session_id: str) -> List[dict]:
        """
        Get all cart items for a given session, joined with product and images.
        """
        response = (
            self.db.table("cart_items")
            .select(
                "*, products(id, name, slug, price, product_images(id, image_url, display_order))"
            )
            .eq("session_id", session_id)
            .order("created_at", desc=False)
            .execute()
        )
        return response.data

    def find_item(self, session_id: str, product_id: str, size: str) -> Optional[dict]:
        """
        Find a specific cart item by session_id, product_id, and size.
        """
        response = (
            self.db.table("cart_items")
            .select("*")
            .eq("session_id", session_id)
            .eq("product_id", product_id)
            .eq("size", size)
            .execute()
        )
        return response.data[0] if response.data else None

    def find_item_by_id(self, item_id: str) -> Optional[dict]:
        """
        Find a cart item by its UUID.
        """
        response = (
            self.db.table("cart_items").select("*").eq("id", item_id).execute()
        )
        return response.data[0] if response.data else None

    def add_item(self, session_id: str, product_id: str, size: str, quantity: int) -> dict:
        """
        Insert a new cart item. If the item (session_id, product_id, size) already exists,
        upsert to update the quantity instead.
        """
        existing = self.find_item(session_id, product_id, size)
        if existing:
            new_quantity = existing["quantity"] + quantity
            return self.update_quantity(existing["id"], new_quantity)

        response = (
            self.db.table("cart_items")
            .insert(
                {
                    "session_id": session_id,
                    "product_id": product_id,
                    "size": size,
                    "quantity": quantity,
                }
            )
            .execute()
        )
        return response.data[0]

    def update_quantity(self, item_id: str, quantity: int) -> dict:
        """
        Update the quantity of an existing cart item by ID.
        """
        response = (
            self.db.table("cart_items")
            .update({"quantity": quantity})
            .eq("id", item_id)
            .execute()
        )
        return response.data[0]

    def remove_item(self, item_id: str) -> None:
        """
        Delete a cart item by ID.
        """
        self.db.table("cart_items").delete().eq("id", item_id).execute()

    def clear_cart(self, session_id: str) -> None:
        """
        Remove all cart items for a session (used after checkout).
        """
        self.db.table("cart_items").delete().eq("session_id", session_id).execute()
