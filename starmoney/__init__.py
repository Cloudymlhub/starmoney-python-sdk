"""
StarMoney Python SDK

Official async Python client for StarMoney Bank API.

Quick Start:
    ```python
    from starmoney import StarmoneyClient
    
    async with StarmoneyClient(
        jwt_secret="your-secret",
        issuer="your-service"
    ) as client:
        # Create account
        account = await client.accounts.create(...)
        
        # Send payment
        payment = await client.payments.send(...)
        
        # Check status
        status = await client.payments.get_status(...)
    ```

Webhook Validation:
    ```python
    from starmoney.webhooks import WebhookValidator
    
    validator = WebhookValidator(webhook_secret="your-secret")
    event = validator.parse_webhook(payload, signature)
    ```
"""

from .client import StarmoneyClient
from .webhooks.validator import WebhookValidator
from .exceptions import (
    StarmoneyError,
    APIError,
    AuthenticationError,
    ValidationError,
    PaymentNotFoundError,
    DuplicateResourceError,
    RateLimitError,
    ServerError,
    InvalidSignatureError,
)

__version__ = "0.1.0"
__all__ = [
    "StarmoneyClient",
    "WebhookValidator",
    "StarmoneyError",
    "APIError",
    "AuthenticationError",
    "ValidationError",
    "PaymentNotFoundError",
    "DuplicateResourceError",
    "RateLimitError",
    "ServerError",
    "InvalidSignatureError",
]
