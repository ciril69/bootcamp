from typing import Any, Dict

def format_success_response(data: Any = None, message: str = None) -> Dict[str, Any]:
    """
    Format standard success response JSON.
    """
    response = {"success": True}
    if data is not None:
        response["data"] = data
    if message is not None:
        response["message"] = message
    return response
