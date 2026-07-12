from typing import List, Optional
from supabase import Client
from app.db.client import supabase as default_supabase

class CategoryRepository:
    """
    Repository class for managing Categories via Supabase.
    """
    def __init__(self, db: Optional[Client] = None) -> None:
        self.db = db if db is not None else default_supabase

    def get_all(self) -> List[dict]:
        """
        Get all categories from the database.
        """
        response = self.db.table("categories").select("*").execute()
        return response.data

    def find_by_id(self, category_id: str) -> Optional[dict]:
        """
        Retrieve a single category by ID.
        """
        response = self.db.table("categories").select("*").eq("id", category_id).execute()
        return response.data[0] if response.data else None

    def find_by_slug(self, slug: str) -> Optional[dict]:
        """
        Retrieve a single category by slug.
        """
        response = self.db.table("categories").select("*").eq("slug", slug).execute()
        return response.data[0] if response.data else None
