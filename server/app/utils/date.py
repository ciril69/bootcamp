from datetime import datetime

def format_datetime(dt: datetime) -> str:
    """
    Format a datetime object to standard ISO 8601 string.
    """
    return dt.isoformat()
