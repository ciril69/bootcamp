from typing import Any, List
from pydantic import BaseModel

class PaginationResponse(BaseModel):
    """
    Pydantic schema representing generic paginated data responses.
    """
    items: List[Any]
    total: int
    page: int
    limit: int
    pages: int
