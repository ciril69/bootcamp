from typing import Optional
from loguru import logger
from app.repositories.contact import ContactRepository
from app.schemas.contact import ContactRequest, ContactResponse
from app.constants import API_MSG_CONTACT_SUCCESS


class ContactService:
    """
    Service class for Contact business logic.
    Validates and persists contact form submissions.
    """

    def __init__(self, contact_repo: Optional[ContactRepository] = None) -> None:
        self.contact_repo = contact_repo or ContactRepository()

    def submit_contact(self, request: ContactRequest) -> ContactResponse:
        """
        Save a contact form submission to the database and return a confirmation.
        Pydantic has already validated email and phone at the schema level.
        """
        logger.info(f"New contact form submission from: {request.email}")

        self.contact_repo.save_message(
            name=request.name,
            email=request.email,
            message=request.message,
            phone=request.phone,
        )

        return ContactResponse(
            success=True,
            message=API_MSG_CONTACT_SUCCESS,
        )
