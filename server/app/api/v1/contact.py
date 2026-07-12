"""
Contact Router
--------------
POST /contact – Store a contact / customisation inquiry in the database.
"""
from fastapi import APIRouter, status

from app.schemas.contact import ContactRequest, ContactResponse
from app.services.contact import ContactService

router = APIRouter(prefix="/contact", tags=["Contact"])
_svc = ContactService()


@router.post(
    "",
    summary="Submit Contact Form",
    description=(
        "Store a contact or customisation inquiry. "
        "Validates name, email, optional phone, and message. "
        "Returns a confirmation on success."
    ),
    response_model=ContactResponse,
    status_code=status.HTTP_201_CREATED,
    responses={
        201: {"description": "Message received and stored"},
        422: {"description": "Validation error"},
    },
)
async def submit_contact(body: ContactRequest) -> ContactResponse:
    """Accept and persist a contact form submission."""
    return _svc.submit_contact(body)
