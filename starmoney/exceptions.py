"""StarMoney Python SDK - Custom Exceptions"""

from typing import Any, Optional


class StarmoneyError(Exception):
    """Base exception for all StarMoney SDK errors."""
    pass


class APIError(StarmoneyError):
    """
    Error from StarMoney API response.
    
    Attributes:
        status_code: HTTP status code
        message: Error message
        response_data: Full response data from API
    """
    
    def __init__(self, status_code: int, message: str, response_data: Optional[dict[str, Any]] = None):
        self.status_code = status_code
        self.message = message
        self.response_data = response_data or {}
        super().__init__(f"[{status_code}] {message}")


class AuthenticationError(APIError):
    """401 - Invalid or expired authentication credentials."""
    pass


class ValidationError(APIError):
    """400 - Invalid request data or parameters."""
    pass


class PaymentNotFoundError(APIError):
    """404 - Payment not found."""
    pass


class DuplicateResourceError(APIError):
    """409 - Resource already exists (e.g., duplicate payment)."""
    pass


class RateLimitError(APIError):
    """429 - Too many requests."""
    pass


class ServerError(APIError):
    """500+ - Internal server error."""
    pass


class InvalidSignatureError(StarmoneyError):
    """Webhook signature validation failed."""
    pass
