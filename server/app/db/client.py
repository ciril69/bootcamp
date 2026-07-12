from supabase import create_client, Client
from app.config import get_settings
from loguru import logger

settings = get_settings()

# Reusable client instance
supabase: Client = None

try:
    if settings.SUPABASE_URL and settings.SUPABASE_ANON_KEY:
        supabase = create_client(settings.SUPABASE_URL, settings.SUPABASE_ANON_KEY)
        logger.info("Supabase client initialized successfully.")
    else:
        logger.warning("SUPABASE_URL and SUPABASE_ANON_KEY are missing. Supabase client not initialized.")
except Exception as e:
    logger.exception("Failed to initialize Supabase client")
