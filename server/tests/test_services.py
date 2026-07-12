"""
Unit tests for service classes using mocked repositories.
These tests verify business logic (validation, error raising, computation)
without touching the database.
"""

import pytest
from decimal import Decimal
from unittest.mock import MagicMock, patch
from app.services.category import CategoryService
from app.services.product import ProductService
from app.services.cart import CartService
from app.services.order import OrderService
from app.services.contact import ContactService
from app.exceptions import (
    CategoryNotFound,
    ProductNotFound,
    CartNotFound,
    OrderNotFound,
    InvalidQuantity,
)
from app.schemas.order import CheckoutRequest
from app.schemas.contact import ContactRequest


# ---------------------------------------------------------------------------
# CategoryService
# ---------------------------------------------------------------------------

class TestCategoryService:
    def test_get_all_returns_list(self):
        mock_repo = MagicMock()
        mock_repo.get_all.return_value = [{"name": "T-Shirts"}]
        svc = CategoryService(category_repo=mock_repo)
        result = svc.get_all_categories()
        assert result == [{"name": "T-Shirts"}]

    def test_get_by_slug_found(self):
        mock_repo = MagicMock()
        mock_repo.find_by_slug.return_value = {"id": "1", "slug": "t-shirts"}
        svc = CategoryService(category_repo=mock_repo)
        result = svc.get_category_by_slug("t-shirts")
        assert result["slug"] == "t-shirts"

    def test_get_by_slug_not_found_raises(self):
        mock_repo = MagicMock()
        mock_repo.find_by_slug.return_value = None
        svc = CategoryService(category_repo=mock_repo)
        with pytest.raises(CategoryNotFound):
            svc.get_category_by_slug("unknown")

    def test_get_by_id_not_found_raises(self):
        mock_repo = MagicMock()
        mock_repo.find_by_id.return_value = None
        svc = CategoryService(category_repo=mock_repo)
        with pytest.raises(CategoryNotFound):
            svc.get_category_by_id("nonexistent-uuid")


# ---------------------------------------------------------------------------
# ProductService
# ---------------------------------------------------------------------------

class TestProductService:
    def test_get_product_found(self):
        mock_repo = MagicMock()
        mock_repo.find_by_slug.return_value = {
            "id": "p1", "slug": "my-tee", "category_id": "c1"
        }
        mock_repo.get_related.return_value = []
        svc = ProductService(product_repo=mock_repo)
        result = svc.get_product("my-tee")
        assert result["slug"] == "my-tee"
        assert "related_products" in result

    def test_get_product_not_found_raises(self):
        mock_repo = MagicMock()
        mock_repo.find_by_slug.return_value = None
        svc = ProductService(product_repo=mock_repo)
        with pytest.raises(ProductNotFound):
            svc.get_product("nonexistent-slug")

    def test_get_featured_returns_list(self):
        mock_repo = MagicMock()
        mock_repo.get_featured.return_value = [{"id": "p1", "featured": True}]
        svc = ProductService(product_repo=mock_repo)
        result = svc.get_featured_products()
        assert len(result) == 1


# ---------------------------------------------------------------------------
# CartService
# ---------------------------------------------------------------------------

class TestCartService:
    def test_get_cart_computes_subtotal(self):
        mock_cart_repo = MagicMock()
        mock_cart_repo.get_cart_items.return_value = [
            {"id": "ci1", "quantity": 2, "size": "M",
             "products": {"id": "p1", "price": "30.00"}},
        ]
        svc = CartService(cart_repo=mock_cart_repo)
        result = svc.get_cart("sess-1")
        assert result["subtotal"] == Decimal("60.00")

    def test_add_item_invalid_quantity_raises(self):
        svc = CartService()
        with pytest.raises(InvalidQuantity):
            svc.add_item("sess-1", "prod-1", "M", 0)

    def test_add_item_product_not_found_raises(self):
        mock_cart_repo = MagicMock()
        mock_product_repo = MagicMock()
        mock_product_repo.find_by_id.return_value = None
        svc = CartService(cart_repo=mock_cart_repo, product_repo=mock_product_repo)
        with pytest.raises(ProductNotFound):
            svc.add_item("sess-1", "nonexistent-prod", "M", 1)

    def test_update_quantity_item_not_found_raises(self):
        mock_cart_repo = MagicMock()
        mock_cart_repo.find_item_by_id.return_value = None
        svc = CartService(cart_repo=mock_cart_repo)
        with pytest.raises(CartNotFound):
            svc.update_quantity("nonexistent-item", 2)

    def test_update_quantity_invalid_raises(self):
        svc = CartService()
        with pytest.raises(InvalidQuantity):
            svc.update_quantity("some-item", 0)

    def test_remove_item_not_found_raises(self):
        mock_cart_repo = MagicMock()
        mock_cart_repo.find_item_by_id.return_value = None
        svc = CartService(cart_repo=mock_cart_repo)
        with pytest.raises(CartNotFound):
            svc.remove_item("nonexistent-item")


# ---------------------------------------------------------------------------
# OrderService
# ---------------------------------------------------------------------------

class TestOrderService:
    def test_submit_order_empty_cart_raises(self):
        mock_cart_repo = MagicMock()
        mock_cart_repo.get_cart_items.return_value = []
        svc = OrderService(cart_repo=mock_cart_repo)
        checkout = CheckoutRequest(
            session_id="sess-1",
            customer_name="Jane",
            email="jane@example.com",
            phone="+919876543210",
            address="123 Main Street",
        )
        with pytest.raises(CartNotFound):
            svc.submit_order(checkout)

    def test_submit_order_success(self):
        mock_cart_repo = MagicMock()
        mock_cart_repo.get_cart_items.return_value = [
            {
                "id": "ci1",
                "product_id": "prod-1",
                "quantity": 1,
                "size": "L",
                "products": {"id": "prod-1", "price": "59.99"},
            }
        ]
        mock_order_repo = MagicMock()
        mock_order_repo.create_order.return_value = {"id": "a1b2c3d4-e5f6-7890-abcd-ef1234567890"}
        mock_order_repo.create_order_items.return_value = [{}]

        svc = OrderService(
            order_repo=mock_order_repo,
            cart_repo=mock_cart_repo,
        )
        checkout = CheckoutRequest(
            session_id="sess-1",
            customer_name="Jane",
            email="jane@example.com",
            phone="+919876543210",
            address="123 Main Street",
        )
        result = svc.submit_order(checkout)
        assert result.success is True
        assert result.order_id is not None
        # Cart should be cleared
        mock_cart_repo.clear_cart.assert_called_once_with("sess-1")

    def test_get_order_not_found_raises(self):
        mock_order_repo = MagicMock()
        mock_order_repo.find_by_id.return_value = None
        svc = OrderService(order_repo=mock_order_repo)
        with pytest.raises(OrderNotFound):
            svc.get_order("nonexistent-order")


# ---------------------------------------------------------------------------
# ContactService
# ---------------------------------------------------------------------------

class TestContactService:
    def test_submit_contact_success(self):
        mock_repo = MagicMock()
        mock_repo.save_message.return_value = {"id": "msg-1"}
        svc = ContactService(contact_repo=mock_repo)
        request = ContactRequest(
            name="Alex",
            email="alex@example.com",
            phone="+919876543210",
            message="Custom hoodie enquiry",
        )
        result = svc.submit_contact(request)
        assert result.success is True
        mock_repo.save_message.assert_called_once()
