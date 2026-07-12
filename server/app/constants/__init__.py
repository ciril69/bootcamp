from typing import Final

# Product sizes available
AVAILABLE_SIZES: Final[list[str]] = ["S", "M", "L", "XL", "XXL"]

# Order status values
DEFAULT_ORDER_STATUS: Final[str] = "demo"
ORDER_STATUSES: Final[list[str]] = ["demo", "pending", "processing", "shipped", "delivered", "cancelled"]

# Pagination settings
DEFAULT_PAGE: Final[int] = 1
DEFAULT_LIMIT: Final[int] = 10

# API Messages
API_MSG_ORDER_SUCCESS: Final[str] = "Demo order submitted successfully."
API_MSG_CONTACT_SUCCESS: Final[str] = "Contact message submitted successfully."

# Category constants mapping slug to name
CATEGORIES: Final[dict[str, str]] = {
    "oversized-t-shirts": "Oversized T-Shirts",
    "oversized-hoodies": "Oversized Hoodies",
    "tank-tops": "Tank Tops",
    "jackets": "Jackets",
}
