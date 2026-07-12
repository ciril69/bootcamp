from typing import Any, Optional
from supabase import Client
from app.db.client import supabase as default_supabase


class ContactRepository:
    """
    Repository class for managing Contact Messages via Supabase.
    No business logic — only raw Supabase data access.
    """

    def __init__(self, db: Optional[Client] = None) -> None:
        self.db = db if db is not None else default_supabase

    def save_message(
        self,
        name: str,
        email: str,
        message: str,
        phone: Optional[str] = None,
    ) -> dict:
        """
        Insert a new contact message into the database.
        """
        payload: dict[str, Any] = {
            "name": name,
            "email": email,
            "message": message,
        }
        if phone:
            payload["phone"] = phone

        response = self.db.table("contact_messages").insert(payload).execute()
        return response.data[0]
