from uuid import UUID

def is_valid_uuid(val: str) -> bool:
    """
    Check if a string is a valid UUID version 4.
    """
    try:
        UUID(str(val))
        return True
    except ValueError:
        return False
