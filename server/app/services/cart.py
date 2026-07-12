from decimal import Decimal
from typing import Optional
from loguru import logger
from app.repositories.cart import CartRepository
from app.repositories.product import ProductRepository
from app.exceptions import CartNotFound, ProductNotFound, InvalidQuantity
from app.schemas.cart import Cart, CartItem
from app.utils.price import format_price


class CartService:
    """
    Service class for Cart business logic.
    Validates products exist, enforces quantity rules, and computes subtotals.
    """

    def __init__(
        self,
        cart_repo: Optional[CartRepository] = None,
        product_repo: Optional[ProductRepository] = None,
    ) -> None:
        self.cart_repo = cart_repo or CartRepository()
        self.product_repo = product_repo or ProductRepository()

    def get_cart(self, session_id: str) -> dict:
        """
        Return all cart items for the session along with the computed subtotal.
        """
        logger.debug(f"Fetching cart for session: {session_id}")
        items = self.cart_repo.get_cart_items(session_id)

        subtotal = Decimal("0.00")
        for item in items:
            product = item.get("products") or {}
            price = Decimal(str(product.get("price", 0)))
            qty = item.get("quantity", 0)
            subtotal += price * qty

        return {
            "session_id": session_id,
            "items": items,
            "subtotal": format_price(subtotal),
        }

    def add_item(
        self, session_id: str, product_id: str, size: str, quantity: int
    ) -> dict:
        """
        Add an item to the cart. Validates that the product exists and quantity > 0.
        If the item already exists, merges quantity.
        """
        if quantity < 1:
            raise InvalidQuantity("Quantity must be at least 1.")

        # Validate product exists
        product = self.product_repo.find_by_id(product_id)
        if not product:
            raise ProductNotFound(f"Product '{product_id}' not found.")

        logger.debug(
            f"Adding to cart: session={session_id} product={product_id} size={size} qty={quantity}"
        )
        item = self.cart_repo.add_item(session_id, product_id, size, quantity)
        return item

    def update_quantity(self, item_id: str, quantity: int) -> dict:
        """
        Update quantity of an existing cart item. Raises CartNotFound if item not found.
        """
        if quantity < 1:
            raise InvalidQuantity("Quantity must be at least 1.")

        existing = self.cart_repo.find_item_by_id(item_id)
        if not existing:
            raise CartNotFound(f"Cart item '{item_id}' not found.")

        logger.debug(f"Updating cart item {item_id} quantity to {quantity}")
        return self.cart_repo.update_quantity(item_id, quantity)

    def remove_item(self, item_id: str) -> None:
        """
        Remove a cart item by ID. Raises CartNotFound if it doesn't exist.
        """
        existing = self.cart_repo.find_item_by_id(item_id)
        if not existing:
            raise CartNotFound(f"Cart item '{item_id}' not found.")

        logger.debug(f"Removing cart item: {item_id}")
        self.cart_repo.remove_item(item_id)
