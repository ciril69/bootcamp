from typing import List, Optional
from loguru import logger
from app.repositories.category import CategoryRepository
from app.exceptions import CategoryNotFound
from app.schemas.category import Category


class CategoryService:
    """
    Service class for Category business logic.
    Handles validation, error raising, and repository coordination.
    """

    def __init__(self, category_repo: Optional[CategoryRepository] = None) -> None:
        self.category_repo = category_repo or CategoryRepository()

    def get_all_categories(self) -> List[dict]:
        """
        Return all categories.
        """
        logger.debug("Fetching all categories")
        return self.category_repo.get_all()

    def get_category_by_id(self, category_id: str) -> dict:
        """
        Return a category by ID, raising CategoryNotFound if it doesn't exist.
        """
        logger.debug(f"Fetching category by id: {category_id}")
        category = self.category_repo.find_by_id(category_id)
        if not category:
            raise CategoryNotFound(f"Category with id '{category_id}' not found.")
        return category

    def get_category_by_slug(self, slug: str) -> dict:
        """
        Return a category by slug, raising CategoryNotFound if it doesn't exist.
        """
        logger.debug(f"Fetching category by slug: {slug}")
        category = self.category_repo.find_by_slug(slug)
        if not category:
            raise CategoryNotFound(f"Category with slug '{slug}' not found.")
        return category
