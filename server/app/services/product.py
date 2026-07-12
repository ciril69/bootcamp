from app.repositories.product import ProductRepository

class ProductService:
    """
    Service class for Product business logic.
    Currently empty scaffolding.
    """
    def __init__(self, product_repo: ProductRepository) -> None:
        self.product_repo = product_repo
