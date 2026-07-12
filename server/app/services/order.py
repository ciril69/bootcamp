from decimal import Decimal
from typing import Optional
from loguru import logger
from app.repositories.order import OrderRepository
from app.repositories.cart import CartRepository
from app.repositories.product import ProductRepository
from app.exceptions import OrderNotFound, CartNotFound, ValidationException
from app.schemas.order import CheckoutRequest, CheckoutResponse
from app.utils.price import format_price
from app.constants import API_MSG_ORDER_SUCCESS


class OrderService:
    """
    Service class for Order business logic.
    Handles checkout flow: validates cart, computes total, creates order + items, clears cart.
    """

    def __init__(
        self,
        order_repo: Optional[OrderRepository] = None,
        cart_repo: Optional[CartRepository] = None,
        product_repo: Optional[ProductRepository] = None,
    ) -> None:
        self.order_repo = order_repo or OrderRepository()
        self.cart_repo = cart_repo or CartRepository()
        self.product_repo = product_repo or ProductRepository()

    def submit_order(self, checkout: CheckoutRequest) -> CheckoutResponse:
        """
        Process a demo checkout:
        1. Fetch cart items for the session.
        2. Validate cart is not empty.
        3. Compute total from cart items × product prices.
        4. Create order record.
        5. Create order_items records.
        6. Clear the cart.
        7. Return confirmation.
        """
        logger.info(f"Processing checkout for session: {checkout.session_id}")

        # 1. Fetch cart items
        cart_items = self.cart_repo.get_cart_items(checkout.session_id)
        if not cart_items:
            raise CartNotFound(
                "No items found in cart. Please add products before checking out."
            )

        # 2. Compute total
        total = Decimal("0.00")
        order_items_payload = []

        for item in cart_items:
            product = item.get("products") or {}
            if not product:
                raise ValidationException(
                    f"Product data missing for cart item '{item.get('id')}'."
                )
            unit_price = Decimal(str(product.get("price", 0)))
            qty = item.get("quantity", 1)
            total += unit_price * qty
            order_items_payload.append(
                {
                    "product_id": item["product_id"],
                    "quantity": qty,
                    "size": item["size"],
                    "unit_price": float(unit_price),
                }
            )

        # 3. Create order record
        order = self.order_repo.create_order(
            session_id=checkout.session_id,
            customer_name=checkout.customer_name,
            email=checkout.email,
            phone=checkout.phone,
            address=checkout.address,
            total_amount=float(format_price(total)),
        )

        # 4. Attach order_id to each order item
        for oi in order_items_payload:
            oi["order_id"] = order["id"]

        # 5. Persist order items
        self.order_repo.create_order_items(order_items_payload)

        # 6. Clear the cart
        self.cart_repo.clear_cart(checkout.session_id)

        logger.info(f"Order created successfully: {order['id']}")
        return CheckoutResponse(
            success=True,
            message=API_MSG_ORDER_SUCCESS,
            order_id=order["id"],
        )

    def get_order(self, order_id: str) -> dict:
        """
        Return order details by ID. Raises OrderNotFound if not found.
        """
        logger.debug(f"Fetching order: {order_id}")
        order = self.order_repo.find_by_id(order_id)
        if not order:
            raise OrderNotFound(f"Order '{order_id}' not found.")
        return order
