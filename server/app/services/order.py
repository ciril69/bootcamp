from app.repositories.order import OrderRepository

class OrderService:
    """
    Service class for Order business logic.
    Currently empty scaffolding.
    """
    def __init__(self, order_repo: OrderRepository) -> None:
        self.order_repo = order_repo
