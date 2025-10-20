"""
StarMoney Python SDK - Authentication Manager

Handles JWT token generation for service-to-service and user authentication.
Matches the authentication pattern from the StarMoney Bank Service.
"""

from datetime import datetime, timedelta, timezone
from typing import Optional
from jose import jwt


class AuthManager:
    """
    Manages JWT token generation for StarMoney API authentication.

    Supports two authentication modes:
    1. Service tokens (iss claim only) - for service-to-service calls
    2. User tokens (sub + iss claims) - for user-scoped operations
    """

    def __init__(self, jwt_secret: str, issuer: str = "starmoney-sdk"):
        """
        Initialize authentication manager.

        Args:
            jwt_secret: Secret key for signing JWTs (must match server configuration)
            issuer: Issuer identifier for JWT claims (must be registered with StarMoney)
        """
        self.jwt_secret = jwt_secret
        self.issuer = issuer
        self.algorithm = "HS256"
        self.token_expiry_hours = 1

    def create_service_token(self) -> str:
        """
        Create a service-level JWT token for service-to-service authentication.

        Used for operations like:
        - Creating user accounts
        - Batch webhook subscriptions
        - Admin operations

        Returns:
            Signed JWT token string
        """
        payload = {
            "iss": self.issuer,
            "exp": datetime.now(timezone.utc) + timedelta(hours=self.token_expiry_hours),
            "iat": datetime.now(timezone.utc),
        }
        return jwt.encode(payload, self.jwt_secret, algorithm=self.algorithm)

    def create_user_token(self, user_id: str) -> str:
        """
        Create a user-scoped JWT token for user-specific operations.

        Used for operations like:
        - Sending payments (as specific user)
        - Creating beneficiaries
        - Checking payment status

        Args:
            user_id: UUID of the user to authenticate as

        Returns:
            Signed JWT token string
        """
        payload = {
            "sub": user_id,
            "iss": self.issuer,
            "exp": datetime.now(timezone.utc) + timedelta(hours=self.token_expiry_hours),
            "iat": datetime.now(timezone.utc),
        }
        return jwt.encode(payload, self.jwt_secret, algorithm=self.algorithm)

    def get_auth_header(self, user_id: Optional[str] = None) -> dict[str, str]:
        """
        Get HTTP authorization header for API requests.

        Args:
            user_id: Optional user ID for user-scoped operations.
                    If None, creates service-level token.

        Returns:
            Dictionary with Authorization header
        """
        if user_id:
            token = self.create_user_token(user_id)
        else:
            token = self.create_service_token()

        return {"Authorization": f"Bearer {token}"}
