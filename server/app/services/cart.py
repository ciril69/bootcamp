from app.repositories.cart import CartRepository

class CartService:
    """
    Service class for Cart business logic.
    Currently empty scaffolding.
    """
    def __init__(self, cart_repo: CartRepository) -> None:
        self.cart_repo = cart_repo
