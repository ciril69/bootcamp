"""
Endpoint tests – Phase 3
========================
Tests every HTTP endpoint using FastAPI's TestClient with mocked services,
so no live Supabase connection is required.

Coverage:
  Health      – GET /health, GET /api/v1/health
  Categories  – GET /api/v1/categories
  Products    – GET /api/v1/products, /products/featured, /products/{slug}
  Cart        – GET, POST, PATCH, DELETE
  Orders      – POST /api/v1/orders, GET /api/v1/orders/{id}
  Contact     – POST /api/v1/contact
"""

import pytest
from decimal import Decimal
from unittest.mock import MagicMock, patch
from fastapi.testclient import TestClient

from app.main import app
from app.exceptions import (
    ProductNotFound,
    CartNotFound,
    OrderNotFound,
)
from app.schemas.order import CheckoutResponse
from app.schemas.contact import ContactResponse
from app.schemas.pagination import PaginationResponse


# ---------------------------------------------------------------------------
# Shared fixtures
# ---------------------------------------------------------------------------

@pytest.fixture(scope="module")
def client():
    """Module-scoped TestClient; lifespan events are exercised once."""
    with TestClient(app) as c:
        yield c


# Helpers -------------------------------------------------------------------

def _pagination(items, total=None):
    return PaginationResponse(
        items=items,
        total=total if total is not None else len(items),
        page=1,
        limit=10,
        pages=1,
    )


SAMPLE_CATEGORY = {"id": "cat-1", "name": "T-Shirts", "slug": "t-shirts", "description": None, "created_at": "2024-01-01T00:00:00"}

SAMPLE_PRODUCT = {
    "id": "prod-1",
    "name": "Onyx Tee",
    "slug": "onyx-tee",
    "description": "Heavyweight cotton.",
    "price": "68.00",
    "stock": 10,
    "featured": True,
    "customization_available": True,
    "category_id": "cat-1",
    "created_at": "2024-01-01T00:00:00",
    "categories": {"id": "cat-1", "name": "T-Shirts", "slug": "t-shirts"},
    "product_images": [{"id": "img-1", "image_url": "https://example.com/img.jpg", "display_order": 0}],
    "related_products": [],
}

SAMPLE_CART_ITEM = {
    "id": "item-1",
    "session_id": "sess-abc",
    "product_id": "prod-1",
    "size": "M",
    "quantity": 2,
    "created_at": "2024-01-01T00:00:00",
    "products": {"id": "prod-1", "name": "Onyx Tee", "price": "68.00"},
}

SAMPLE_CART = {
    "session_id": "sess-abc",
    "items": [SAMPLE_CART_ITEM],
    "subtotal": Decimal("136.00"),
}

SAMPLE_ORDER = {
    "id": "order-1",
    "session_id": "sess-abc",
    "customer_name": "John Doe",
    "email": "john@example.com",
    "phone": "+911234567890",
    "address": "123 Main St",
    "total_amount": "136.00",
    "status": "demo",
    "created_at": "2024-01-01T00:00:00",
    "order_items": [],
}


# ===========================================================================
# Health
# ===========================================================================

class TestHealth:
    def test_root_health_ok(self, client):
        r = client.get("/health")
        assert r.status_code == 200
        assert r.json() == {"status": "healthy"}

    def test_v1_health_ok(self, client):
        r = client.get("/api/v1/health")
        assert r.status_code == 200
        assert r.json() == {"status": "healthy"}


# ===========================================================================
# Categories
# ===========================================================================

class TestCategories:
    def test_list_categories_ok(self, client):
        with patch("app.api.v1.categories._svc") as mock_svc:
            mock_svc.get_all_categories.return_value = [SAMPLE_CATEGORY]
            r = client.get("/api/v1/categories")
        assert r.status_code == 200
        body = r.json()
        assert body["success"] is True
        assert isinstance(body["data"], list)
        assert body["data"][0]["slug"] == "t-shirts"

    def test_list_categories_empty(self, client):
        with patch("app.api.v1.categories._svc") as mock_svc:
            mock_svc.get_all_categories.return_value = []
            r = client.get("/api/v1/categories")
        assert r.status_code == 200
        assert r.json()["data"] == []


# ===========================================================================
# Products
# ===========================================================================

class TestProducts:
    # GET /api/v1/products --------------------------------------------------

    def test_list_products_ok(self, client):
        with patch("app.api.v1.products._svc") as mock_svc:
            mock_svc.list_products.return_value = _pagination([SAMPLE_PRODUCT])
            r = client.get("/api/v1/products")
        assert r.status_code == 200
        body = r.json()
        assert body["success"] is True
        assert len(body["data"]) == 1
        assert "pagination" in body
        assert body["pagination"]["total"] == 1

    def test_list_products_with_filters(self, client):
        with patch("app.api.v1.products._svc") as mock_svc:
            mock_svc.list_products.return_value = _pagination([SAMPLE_PRODUCT])
            r = client.get(
                "/api/v1/products",
                params={"category": "t-shirts", "search": "tee", "sort": "price_asc", "page": 1, "limit": 5},
            )
        assert r.status_code == 200
        _, kwargs = mock_svc.list_products.call_args
        assert kwargs["category"] == "t-shirts"
        assert kwargs["sort"] == "price_asc"

    def test_list_products_invalid_sort(self, client):
        r = client.get("/api/v1/products", params={"sort": "invalid_sort"})
        assert r.status_code == 422

    def test_list_products_empty(self, client):
        with patch("app.api.v1.products._svc") as mock_svc:
            mock_svc.list_products.return_value = _pagination([], total=0)
            r = client.get("/api/v1/products")
        assert r.status_code == 200
        assert r.json()["data"] == []
        assert r.json()["pagination"]["total"] == 0

    # GET /api/v1/products/featured ----------------------------------------

    def test_get_featured_ok(self, client):
        with patch("app.api.v1.products._svc") as mock_svc:
            mock_svc.get_featured_products.return_value = [SAMPLE_PRODUCT]
            r = client.get("/api/v1/products/featured")
        assert r.status_code == 200
        body = r.json()
        assert body["success"] is True
        assert len(body["data"]) == 1

    def test_get_featured_empty(self, client):
        with patch("app.api.v1.products._svc") as mock_svc:
            mock_svc.get_featured_products.return_value = []
            r = client.get("/api/v1/products/featured")
        assert r.status_code == 200
        assert r.json()["data"] == []

    def test_get_featured_custom_limit(self, client):
        with patch("app.api.v1.products._svc") as mock_svc:
            mock_svc.get_featured_products.return_value = []
            r = client.get("/api/v1/products/featured", params={"limit": 4})
        assert r.status_code == 200
        mock_svc.get_featured_products.assert_called_once_with(limit=4)

    # GET /api/v1/products/{slug} ------------------------------------------

    def test_get_product_ok(self, client):
        with patch("app.api.v1.products._svc") as mock_svc:
            mock_svc.get_product.return_value = SAMPLE_PRODUCT
            r = client.get("/api/v1/products/onyx-tee")
        assert r.status_code == 200
        body = r.json()
        assert body["success"] is True
        assert body["data"]["slug"] == "onyx-tee"

    def test_get_product_not_found(self, client):
        with patch("app.api.v1.products._svc") as mock_svc:
            mock_svc.get_product.side_effect = ProductNotFound("Not found")
            r = client.get("/api/v1/products/no-such-product")
        assert r.status_code == 404
        body = r.json()
        assert body["success"] is False
        assert body["error"]["code"] == "PRODUCT_NOT_FOUND"


# ===========================================================================
# Cart
# ===========================================================================

class TestCart:
    # GET /api/v1/cart/{session_id} ----------------------------------------

    def test_get_cart_ok(self, client):
        with patch("app.api.v1.cart._svc") as mock_svc:
            mock_svc.get_cart.return_value = SAMPLE_CART
            r = client.get("/api/v1/cart/sess-abc")
        assert r.status_code == 200
        body = r.json()
        assert body["success"] is True
        assert body["data"]["session_id"] == "sess-abc"

    def test_get_cart_empty_session(self, client):
        with patch("app.api.v1.cart._svc") as mock_svc:
            mock_svc.get_cart.return_value = {"session_id": "new-sess", "items": [], "subtotal": Decimal("0.00")}
            r = client.get("/api/v1/cart/new-sess")
        assert r.status_code == 200
        assert r.json()["data"]["items"] == []

    # POST /api/v1/cart ----------------------------------------------------

    def test_add_to_cart_ok(self, client):
        with patch("app.api.v1.cart._svc") as mock_svc:
            mock_svc.add_item.return_value = SAMPLE_CART_ITEM
            r = client.post(
                "/api/v1/cart",
                json={"session_id": "sess-abc", "product_id": "00000000-0000-0000-0000-000000000001", "size": "M", "quantity": 1},
            )
        assert r.status_code == 201
        assert r.json()["success"] is True

    def test_add_to_cart_invalid_quantity(self, client):
        r = client.post(
            "/api/v1/cart",
            json={"session_id": "sess-abc", "product_id": "00000000-0000-0000-0000-000000000001", "size": "M", "quantity": 0},
        )
        assert r.status_code == 422

    def test_add_to_cart_invalid_size(self, client):
        r = client.post(
            "/api/v1/cart",
            json={"session_id": "sess-abc", "product_id": "00000000-0000-0000-0000-000000000001", "size": "INVALID", "quantity": 1},
        )
        assert r.status_code == 422

    def test_add_to_cart_missing_fields(self, client):
        r = client.post("/api/v1/cart", json={"session_id": "sess-abc"})
        assert r.status_code == 422

    def test_add_to_cart_product_not_found(self, client):
        with patch("app.api.v1.cart._svc") as mock_svc:
            mock_svc.add_item.side_effect = ProductNotFound("Product not found")
            r = client.post(
                "/api/v1/cart",
                json={"session_id": "sess-abc", "product_id": "00000000-0000-0000-0000-000000000099", "size": "M", "quantity": 1},
            )
        assert r.status_code == 404

    # PATCH /api/v1/cart/{item_id} -----------------------------------------

    def test_update_cart_item_ok(self, client):
        with patch("app.api.v1.cart._svc") as mock_svc:
            mock_svc.update_quantity.return_value = {**SAMPLE_CART_ITEM, "quantity": 3}
            r = client.patch("/api/v1/cart/item-1", json={"quantity": 3})
        assert r.status_code == 200
        assert r.json()["success"] is True

    def test_update_cart_item_invalid_quantity(self, client):
        r = client.patch("/api/v1/cart/item-1", json={"quantity": 0})
        assert r.status_code == 422

    def test_update_cart_item_not_found(self, client):
        with patch("app.api.v1.cart._svc") as mock_svc:
            mock_svc.update_quantity.side_effect = CartNotFound("Not found")
            r = client.patch("/api/v1/cart/ghost-item", json={"quantity": 2})
        assert r.status_code == 404

    # DELETE /api/v1/cart/{item_id} ----------------------------------------

    def test_remove_cart_item_ok(self, client):
        with patch("app.api.v1.cart._svc") as mock_svc:
            mock_svc.remove_item.return_value = None
            r = client.delete("/api/v1/cart/item-1")
        assert r.status_code == 200
        assert r.json()["success"] is True

    def test_remove_cart_item_not_found(self, client):
        with patch("app.api.v1.cart._svc") as mock_svc:
            mock_svc.remove_item.side_effect = CartNotFound("Not found")
            r = client.delete("/api/v1/cart/ghost-item")
        assert r.status_code == 404


# ===========================================================================
# Orders
# ===========================================================================

VALID_ORDER_PAYLOAD = {
    "session_id": "sess-abc",
    "customer_name": "John Doe",
    "email": "john@example.com",
    "phone": "+911234567890",
    "address": "123 Main Street, Mumbai",
}


class TestOrders:
    # POST /api/v1/orders --------------------------------------------------

    def test_submit_order_ok(self, client):
        mock_response = CheckoutResponse(
            success=True,
            message="Demo order submitted successfully.",
            order_id="a1b2c3d4-e5f6-7890-abcd-ef1234567890",
        )
        with patch("app.api.v1.orders._svc") as mock_svc:
            mock_svc.submit_order.return_value = mock_response
            r = client.post("/api/v1/orders", json=VALID_ORDER_PAYLOAD)
        assert r.status_code == 201
        body = r.json()
        assert body["success"] is True
        assert "order_id" in body

    def test_submit_order_empty_cart(self, client):
        with patch("app.api.v1.orders._svc") as mock_svc:
            mock_svc.submit_order.side_effect = CartNotFound("Cart is empty")
            r = client.post("/api/v1/orders", json=VALID_ORDER_PAYLOAD)
        assert r.status_code == 404

    def test_submit_order_invalid_email(self, client):
        r = client.post("/api/v1/orders", json={**VALID_ORDER_PAYLOAD, "email": "not-an-email"})
        assert r.status_code == 422

    def test_submit_order_invalid_phone(self, client):
        r = client.post("/api/v1/orders", json={**VALID_ORDER_PAYLOAD, "phone": "123"})
        assert r.status_code == 422

    def test_submit_order_missing_fields(self, client):
        r = client.post("/api/v1/orders", json={"session_id": "sess-abc"})
        assert r.status_code == 422

    def test_submit_order_missing_address(self, client):
        payload = {k: v for k, v in VALID_ORDER_PAYLOAD.items() if k != "address"}
        r = client.post("/api/v1/orders", json=payload)
        assert r.status_code == 422

    # GET /api/v1/orders/{order_id} ----------------------------------------

    def test_get_order_ok(self, client):
        with patch("app.api.v1.orders._svc") as mock_svc:
            mock_svc.get_order.return_value = SAMPLE_ORDER
            r = client.get("/api/v1/orders/order-1")
        assert r.status_code == 200
        body = r.json()
        assert body["success"] is True
        assert body["data"]["id"] == "order-1"

    def test_get_order_not_found(self, client):
        with patch("app.api.v1.orders._svc") as mock_svc:
            mock_svc.get_order.side_effect = OrderNotFound("Not found")
            r = client.get("/api/v1/orders/no-such-order")
        assert r.status_code == 404
        body = r.json()
        assert body["success"] is False
        assert body["error"]["code"] == "ORDER_NOT_FOUND"


# ===========================================================================
# Contact
# ===========================================================================

VALID_CONTACT_PAYLOAD = {
    "name": "Alex Smith",
    "email": "alex@example.com",
    "phone": "+919876543210",
    "message": "I would like a custom oversized hoodie with embroidery.",
}


@pytest.fixture(autouse=False)
def reset_rate_limiter():
    """Clear the in-memory rate-limit store before each test that needs it."""
    from app.middleware.rate_limit import _store
    _store.clear()
    yield
    _store.clear()


class TestContact:
    @pytest.fixture(autouse=True)
    def _clear_limiter(self, reset_rate_limiter):
        """Auto-reset the rate limiter before every test in this class."""

    def test_submit_contact_ok(self, client):
        mock_response = ContactResponse(success=True, message="Your message has been received.")
        with patch("app.api.v1.contact._svc") as mock_svc:
            mock_svc.submit_contact.return_value = mock_response
            r = client.post("/api/v1/contact", json=VALID_CONTACT_PAYLOAD)
        assert r.status_code == 201
        body = r.json()
        assert body["success"] is True
        assert "message" in body

    def test_submit_contact_without_phone(self, client):
        """Phone is optional — omitting it must succeed."""
        mock_response = ContactResponse(success=True, message="Your message has been received.")
        payload = {k: v for k, v in VALID_CONTACT_PAYLOAD.items() if k != "phone"}
        with patch("app.api.v1.contact._svc") as mock_svc:
            mock_svc.submit_contact.return_value = mock_response
            r = client.post("/api/v1/contact", json=payload)
        assert r.status_code == 201

    def test_submit_contact_invalid_email(self, client):
        r = client.post("/api/v1/contact", json={**VALID_CONTACT_PAYLOAD, "email": "bad-email"})
        assert r.status_code == 422

    def test_submit_contact_empty_message(self, client):
        """Empty string message fails min_length=1 validation."""
        r = client.post("/api/v1/contact", json={**VALID_CONTACT_PAYLOAD, "message": ""})
        assert r.status_code == 422

    def test_submit_contact_missing_name(self, client):
        payload = {k: v for k, v in VALID_CONTACT_PAYLOAD.items() if k != "name"}
        r = client.post("/api/v1/contact", json=payload)
        assert r.status_code == 422

    def test_submit_contact_missing_message(self, client):
        payload = {k: v for k, v in VALID_CONTACT_PAYLOAD.items() if k != "message"}
        r = client.post("/api/v1/contact", json=payload)
        assert r.status_code == 422

    def test_submit_contact_invalid_phone(self, client):
        r = client.post("/api/v1/contact", json={**VALID_CONTACT_PAYLOAD, "phone": "not-a-number"})
        assert r.status_code == 422


# ===========================================================================
# Error format consistency
# ===========================================================================

class TestErrorFormat:
    """Verify that all error responses follow the {success, error: {code, message}} shape."""

    def test_404_has_error_shape(self, client):
        with patch("app.api.v1.products._svc") as mock_svc:
            mock_svc.get_product.side_effect = ProductNotFound()
            r = client.get("/api/v1/products/ghost-slug")
        body = r.json()
        assert body["success"] is False
        assert "error" in body
        assert "code" in body["error"]
        assert "message" in body["error"]

    def test_422_has_error_shape(self, client):
        r = client.post("/api/v1/contact", json={"name": "", "email": "x", "message": "x"})
        body = r.json()
        assert body["success"] is False
        assert "error" in body

    def test_unknown_route_returns_404(self, client):
        r = client.get("/api/v1/nonexistent-endpoint")
        assert r.status_code == 404
