from typing import Any, Dict, List, Optional
from supabase import Client
from app.db.client import supabase as default_supabase


class OrderRepository:
    """
    Repository class for managing Orders and Order Items via Supabase.
    No business logic — only raw Supabase data access.
    """

    def __init__(self, db: Optional[Client] = None) -> None:
        self.db = db if db is not None else default_supabase

    def create_order(
        self,
        session_id: str,
        customer_name: str,
        email: str,
        phone: str,
        address: str,
        total_amount: float,
        status: str = "demo",
    ) -> dict:
        """
        Insert a new order record and return the created order.
        """
        response = (
            self.db.table("orders")
            .insert(
                {
                    "session_id": session_id,
                    "customer_name": customer_name,
                    "email": email,
                    "phone": phone,
                    "address": address,
                    "total_amount": float(total_amount),
                    "status": status,
                }
            )
            .execute()
        )
        return response.data[0]

    def create_order_items(self, items: List[Dict[str, Any]]) -> List[dict]:
        """
        Bulk-insert order items for a given order.
        Each item dict must have: order_id, product_id, quantity, size, unit_price.
        """
        response = self.db.table("order_items").insert(items).execute()
        return response.data

    def find_by_id(self, order_id: str) -> Optional[dict]:
        """
        Get an order by ID, including its order items with product details.
        """
        response = (
            self.db.table("orders")
            .select(
                "*, order_items(id, product_id, quantity, size, unit_price, products(id, name, slug))"
            )
            .eq("id", order_id)
            .execute()
        )
        return response.data[0] if response.data else None
