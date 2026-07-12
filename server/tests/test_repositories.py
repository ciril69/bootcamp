"""
Unit tests for repository classes using mocked Supabase clients.
These tests verify the repository methods call the correct Supabase operations
without requiring a live database connection.
"""

import pytest
from unittest.mock import MagicMock, patch
from app.repositories.category import CategoryRepository
from app.repositories.product import ProductRepository
from app.repositories.cart import CartRepository
from app.repositories.order import OrderRepository
from app.repositories.contact import ContactRepository


# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------

@pytest.fixture
def mock_db():
    """Return a MagicMock that simulates a Supabase client."""
    return MagicMock()


def _make_response(data, count=None):
    """Helper to create a mock Supabase response."""
    resp = MagicMock()
    resp.data = data
    resp.count = count if count is not None else len(data)
    return resp


# ---------------------------------------------------------------------------
# CategoryRepository
# ---------------------------------------------------------------------------

class TestCategoryRepository:
    def test_get_all(self, mock_db):
        mock_db.table().select().execute.return_value = _make_response(
            [{"id": "1", "name": "T-Shirts", "slug": "t-shirts"}]
        )
        repo = CategoryRepository(db=mock_db)
        result = repo.get_all()
        assert len(result) == 1
        assert result[0]["slug"] == "t-shirts"

    def test_find_by_slug_found(self, mock_db):
        mock_db.table().select().eq().execute.return_value = _make_response(
            [{"id": "abc", "slug": "t-shirts"}]
        )
        repo = CategoryRepository(db=mock_db)
        result = repo.find_by_slug("t-shirts")
        assert result is not None
        assert result["slug"] == "t-shirts"

    def test_find_by_slug_not_found(self, mock_db):
        mock_db.table().select().eq().execute.return_value = _make_response([])
        repo = CategoryRepository(db=mock_db)
        result = repo.find_by_slug("unknown-slug")
        assert result is None

    def test_find_by_id_found(self, mock_db):
        mock_db.table().select().eq().execute.return_value = _make_response(
            [{"id": "abc123"}]
        )
        repo = CategoryRepository(db=mock_db)
        result = repo.find_by_id("abc123")
        assert result is not None

    def test_find_by_id_not_found(self, mock_db):
        mock_db.table().select().eq().execute.return_value = _make_response([])
        repo = CategoryRepository(db=mock_db)
        result = repo.find_by_id("nonexistent")
        assert result is None


# ---------------------------------------------------------------------------
# ProductRepository
# ---------------------------------------------------------------------------

class TestProductRepository:
    def test_get_featured(self, mock_db):
        mock_db.table().select().eq().order().limit().execute.return_value = _make_response(
            [{"id": "prod1", "featured": True}]
        )
        repo = ProductRepository(db=mock_db)
        result = repo.get_featured(limit=4)
        assert len(result) == 1

    def test_find_by_slug_found(self, mock_db):
        mock_db.table().select().eq().execute.return_value = _make_response(
            [{"id": "prod1", "slug": "my-tee"}]
        )
        repo = ProductRepository(db=mock_db)
        result = repo.find_by_slug("my-tee")
        assert result is not None
        assert result["slug"] == "my-tee"

    def test_find_by_slug_not_found(self, mock_db):
        mock_db.table().select().eq().execute.return_value = _make_response([])
        repo = ProductRepository(db=mock_db)
        result = repo.find_by_slug("no-such-tee")
        assert result is None


# ---------------------------------------------------------------------------
# CartRepository
# ---------------------------------------------------------------------------

class TestCartRepository:
    def test_get_cart_items_empty(self, mock_db):
        mock_db.table().select().eq().order().execute.return_value = _make_response([])
        repo = CartRepository(db=mock_db)
        result = repo.get_cart_items("sess-123")
        assert result == []

    def test_remove_item_calls_delete(self, mock_db):
        mock_db.table().delete().eq().execute.return_value = _make_response([])
        repo = CartRepository(db=mock_db)
        repo.remove_item("item-id-1")
        mock_db.table().delete().eq.assert_called_with("id", "item-id-1")

    def test_clear_cart_calls_delete(self, mock_db):
        mock_db.table().delete().eq().execute.return_value = _make_response([])
        repo = CartRepository(db=mock_db)
        repo.clear_cart("session-abc")
        mock_db.table().delete().eq.assert_called_with("session_id", "session-abc")


# ---------------------------------------------------------------------------
# OrderRepository
# ---------------------------------------------------------------------------

class TestOrderRepository:
    def test_create_order_returns_data(self, mock_db):
        mock_db.table().insert().execute.return_value = _make_response(
            [{"id": "order-1", "status": "demo"}]
        )
        repo = OrderRepository(db=mock_db)
        result = repo.create_order(
            session_id="sess-1",
            customer_name="John",
            email="john@example.com",
            phone="+911234567890",
            address="123 Street",
            total_amount=100.0,
        )
        assert result["id"] == "order-1"
        assert result["status"] == "demo"

    def test_find_by_id_not_found(self, mock_db):
        mock_db.table().select().eq().execute.return_value = _make_response([])
        repo = OrderRepository(db=mock_db)
        result = repo.find_by_id("nonexistent-order")
        assert result is None


# ---------------------------------------------------------------------------
# ContactRepository
# ---------------------------------------------------------------------------

class TestContactRepository:
    def test_save_message_returns_data(self, mock_db):
        mock_db.table().insert().execute.return_value = _make_response(
            [{"id": "msg-1", "name": "Alex", "email": "alex@example.com"}]
        )
        repo = ContactRepository(db=mock_db)
        result = repo.save_message(
            name="Alex",
            email="alex@example.com",
            message="Hello!",
        )
        assert result["id"] == "msg-1"
