from app.repositories.contact import ContactRepository

class ContactService:
    """
    Service class for Contact business logic.
    Currently empty scaffolding.
    """
    def __init__(self, contact_repo: ContactRepository) -> None:
        self.contact_repo = contact_repo
