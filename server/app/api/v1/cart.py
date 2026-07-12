"""
Cart Router
-----------
GET    /cart/{session_id}  – Retrieve cart items + subtotal for a session
POST   /cart               – Add item (merges if same product+size already exists)
PATCH  /cart/{item_id}     – Update item quantity (>= 1)
DELETE /cart/{item_id}     – Remove an item from the cart
"""
from fastapi import APIRouter, status

from app.schemas.cart import CartItemCreate, CartItemUpdate
from app.services.cart import CartService
from app.utils.response import format_success_response

router = APIRouter(prefix="/cart", tags=["Cart"])
_svc = CartService()


@router.get(
    "/{session_id}",
    summary="Get Cart",
    description=(
        "Return all cart items for the given anonymous session, "
        "including product details, quantities, and the computed subtotal."
    ),
    status_code=status.HTTP_200_OK,
    responses={
        200: {"description": "Cart contents returned"},
    },
)
async def get_cart(session_id: str) -> dict:
    """Return cart contents and subtotal for a session."""
    cart = _svc.get_cart(session_id)
    return format_success_response(data=cart)


@router.post(
    "",
    summary="Add Item to Cart",
    description=(
        "Add a product to the cart. "
        "If the same product + size combination already exists for the session "
        "the quantity is incremented rather than creating a duplicate row."
    ),
    status_code=status.HTTP_201_CREATED,
    responses={
        201: {"description": "Item added to cart"},
        404: {"description": "Product not found"},
        422: {"description": "Validation error"},
    },
)
async def add_to_cart(body: CartItemCreate) -> dict:
    """Add (or merge) a product into the session cart."""
    item = _svc.add_item(
        session_id=body.session_id,
        product_id=str(body.product_id),
        size=body.size,
        quantity=body.quantity,
    )
    return format_success_response(data=item)


@router.patch(
    "/{item_id}",
    summary="Update Cart Item Quantity",
    description="Update the quantity of an existing cart item. Quantity must be >= 1.",
    status_code=status.HTTP_200_OK,
    responses={
        200: {"description": "Quantity updated"},
        400: {"description": "Invalid quantity"},
        404: {"description": "Cart item not found"},
        422: {"description": "Validation error"},
    },
)
async def update_cart_item(item_id: str, body: CartItemUpdate) -> dict:
    """Update the quantity of a specific cart item."""
    item = _svc.update_quantity(item_id, body.quantity)
    return format_success_response(data=item)


@router.delete(
    "/{item_id}",
    summary="Remove Cart Item",
    description="Remove a specific item from the cart by its ID.",
    status_code=status.HTTP_200_OK,
    responses={
        200: {"description": "Item removed"},
        404: {"description": "Cart item not found"},
    },
)
async def remove_cart_item(item_id: str) -> dict:
    """Remove an item from the cart."""
    _svc.remove_item(item_id)
    return format_success_response(message="Item removed from cart.")
