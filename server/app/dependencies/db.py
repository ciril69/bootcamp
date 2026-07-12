from typing import Generator
from supabase import Client
from app.db.client import supabase

def get_db() -> Generator[Client, None, None]:
    """
    FastAPI dependency that yields the Supabase client instance.
    """
    yield supabase
