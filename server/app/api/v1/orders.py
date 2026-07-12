"""
Orders Router
-------------
POST /orders              – Submit a demo checkout order
GET  /orders/{order_id}   – Retrieve a specific order (404 if missing)
"""
from fastapi import APIRouter, status

from app.schemas.order import CheckoutRequest, CheckoutResponse
from app.services.order import OrderService
from app.utils.response import format_success_response

router = APIRouter(prefix="/orders", tags=["Orders"])
_svc = OrderService()


@router.post(
    "",
    summary="Submit Demo Order",
    description=(
        "Process a demo checkout. "
        "The backend retrieves the session cart, verifies all products exist, "
        "calculates the total server-side (client-provided prices are ignored), "
        "creates the order and order items, clears the cart, and returns a confirmation. "
        "No payment processing is performed."
    ),
    response_model=CheckoutResponse,
    status_code=status.HTTP_201_CREATED,
    responses={
        201: {"description": "Order created successfully"},
        404: {"description": "Cart is empty or product not found"},
        422: {"description": "Validation error"},
    },
)
async def submit_order(body: CheckoutRequest) -> CheckoutResponse:
    """Submit a demo checkout and create an order."""
    return _svc.submit_order(body)


@router.get(
    "/{order_id}",
    summary="Get Order",
    description=(
        "Return the full order summary including customer information, "
        "ordered products, total, status, and order date. "
        "Returns 404 if the order is not found."
    ),
    status_code=status.HTTP_200_OK,
    responses={
        200: {"description": "Order returned"},
        404: {"description": "Order not found"},
    },
)
async def get_order(order_id: str) -> dict:
    """Return a specific order's details."""
    order = _svc.get_order(order_id)
    return format_success_response(data=order)
