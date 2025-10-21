"""StarMoney SDK - Accounts Resource"""

from typing import Any
from typing import Dict
from ..http_client import HTTPClient


class AccountsResource:
    """
    Accounts resource for user account management.

    Handles:
    - Creating user accounts
    - Linking payment rails to accounts
    """

    def __init__(self, http_client: HTTPClient):
        self.http = http_client

    async def create(
        self,
        first_name: str,
        last_name: str,
        email: str,
        phone_number: str,
        document_type: str,
        document_number: str,
        address: str,
    ) -> dict[str, Any]:
        """
        Create a new user account.

        Args:
            first_name: User's first name
            last_name: User's last name
            email: User's email address
            phone_number: User's phone number (E.164 format recommended)
            document_type: Document type (e.g., 'PASSPORT', 'ID_CARD')
            document_number: Document number
            address: User's address

        Returns:
            Account data including user_id

        Example:
            ```python
            account = await client.accounts.create(
                first_name="John",
                last_name="Doe",
                email="john@example.com",
                phone_number="+1234567890",
                document_type="PASSPORT",
                document_number="AB123456",
                address="123 Main St"
            )
            user_id = account["user_id"]
            ```
        """
        payload = {
            "first_name": first_name,
            "last_name": last_name,
            "email": email,
            "phone_number": phone_number,
            "document_type": document_type,
            "document_number": document_number,
            "address": address,
        }

        response = await self.http.post("/accounts", json=payload)
        return response.json()

    async def link_rail(self, user_id: str, rail_name: str = "BDK") -> dict[str, Any]:
        """
        Link a payment rail to user's account.

        Args:
            user_id: User ID to link rail to
            rail_name: Payment rail name (default: 'BDK')

        Returns:
            Rail link confirmation data

        Example:
            ```python
            await client.accounts.link_rail(user_id, rail_name="BDK")
            ```
        """
        response = await self.http.post(f"/accounts/rails/{rail_name}", user_id=user_id)
        return response.json()

    async def get_transfer_history(self, user_id: str, limit: int = 20, offset: int = 0) -> Dict[str, Any]:
        """
        Retrieve the authenticated user's transfer history.

        Args:
            user_id: User ID to retrieve transfer history for
            limit: number of transfers to return (default 20)
            offset: pagination offset (default 0)

        Returns:
            Parsed JSON response with transfers, limit, offset and user_id
        """
        params = {"limit": limit, "offset": offset}
        response = await self.http.get("/accounts/transfers", params=params, user_id=user_id)
        return response.json()

    async def get_user_by_phone(self, phone_number: str) -> Dict[str, Any] | None:
        """
        Retrieve a user by phone number using the accounts lookup endpoint.

        Args:
            phone_number: Phone number string to lookup (should be in E.164 or service-expected format)

        Returns:
            The parsed JSON response as a dict if found, or None if the API returns 404.
        """
        response = await self.http.get(f"/accounts/lookup/phone/{phone_number}")

        return response.json()

    async def get_user_available_rails(self, user_id: str) -> Dict[str, Any]:
        """
        Get available payment rails for the authenticated user.

        Returns the list of payment rails available to the user based on their
        stored credentials and rail configurations.

        Args:
            user_id: User ID to retrieve available rails for

        Returns:
            Parsed JSON response containing:
            - user_id: The user's ID
            - available_rails: List of rails with name, display info, and credential status
            - total_rails: Total number of rails
            - configured_rails: Number of rails with stored credentials

        Example:
            ```python
            rails = await client.accounts.get_user_available_rails(user_id)
            for rail in rails["available_rails"]:
                print(f"{rail['name']}: {rail['has_credentials']}")
            ```
        """
        response = await self.http.get("/accounts/rails", user_id=user_id)
        return response.json()
