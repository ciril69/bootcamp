from app.repositories.category import CategoryRepository

class CategoryService:
    """
    Service class for Category business logic.
    Currently empty scaffolding.
    """
    def __init__(self, category_repo: CategoryRepository) -> None:
        self.category_repo = category_repo
