from pydantic import BaseModel

class HealthResponse(BaseModel):
    """
    Pydantic schema representing the Health check endpoint response.
    """
    status: str
