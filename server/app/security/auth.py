"""
Security helpers placeholder module.

This module is reserved for future authentication and authorization logic.

Version 1 of this application does not require authentication.
Anonymous carts are identified by a frontend-generated session_id.

Future versions may add:
- JWT token generation and verification (via Supabase Auth)
- Bearer token extraction from request headers
- Role-based access control (RBAC) guards
- Password hashing utilities

No implementation here yet.
"""

from typing import Optional


def extract_bearer_token(authorization_header: Optional[str]) -> Optional[str]:
    """
    Placeholder: Extract a bearer token from the Authorization header.
    Returns None if the header is absent or malformed.
    """
    if not authorization_header or not authorization_header.startswith("Bearer "):
        return None
    return authorization_header.removeprefix("Bearer ").strip()


def verify_jwt_token(token: str) -> Optional[dict]:
    """
    Placeholder: Verify a JWT token and return its decoded payload.
    To be implemented using Supabase Auth in a future version.
    Returns None until authentication is added.
    """
    # TODO: Implement JWT verification using Supabase Auth
    return None
