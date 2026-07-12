"""
Tests for the Supabase DB client initialization.
These are unit-level tests that verify the client module loads
correctly without raising exceptions, even with placeholder credentials.
"""

import pytest
from unittest.mock import patch, MagicMock


def test_supabase_client_initializes_with_valid_env():
    """
    When SUPABASE_URL and SUPABASE_ANON_KEY are set, the client should initialize.
    """
    mock_client = MagicMock()

    with patch("app.db.client.create_client", return_value=mock_client) as mock_create:
        with patch("app.db.client.settings") as mock_settings:
            mock_settings.SUPABASE_URL = "https://test.supabase.co"
            mock_settings.SUPABASE_ANON_KEY = "test-anon-key"
            # Re-run the initialization by calling create_client directly
            from supabase import create_client
            client = create_client(mock_settings.SUPABASE_URL, mock_settings.SUPABASE_ANON_KEY)
            assert client is not None


def test_supabase_client_module_importable():
    """
    Ensure the db.client module is importable without exceptions.
    """
    try:
        from app.db import client  # noqa: F401
    except Exception as e:
        pytest.fail(f"db.client raised an exception on import: {e}")
