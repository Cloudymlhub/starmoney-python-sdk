"""StarMoney SDK - Beneficiaries Resource"""

from typing import Any
from ..http_client import HTTPClient


class BeneficiariesResource:
    """
    Beneficiaries resource for managing payment beneficiaries.

    Handles:
    - Creating beneficiaries
    - Listing user's beneficiaries
    """

    def __init__(self, http_client: HTTPClient):
        self.http = http_client

    async def create(
        self,
        user_id: str,
        name: str,
        iban: str,
        currency: str,
        bank_name: str,
        address: str,
    ) -> dict[str, Any]:
        """
        Create a new beneficiary for user.

        Args:
            user_id: User ID who owns this beneficiary
            name: Beneficiary name
            iban: Beneficiary's IBAN
            currency: Currency code (e.g., 'EUR', 'USD')
            bank_name: Beneficiary's bank name
            address: Beneficiary's address

        Returns:
            Created beneficiary data

        Example:
            ```python
            beneficiary = await client.beneficiaries.create(
                user_id=user_id,
                name="John Doe",
                iban="FR1420041010050500013M02606",
                currency="EUR",
                bank_name="Test Bank",
                address="123 Test Ave"
            )
            ```
        """
        payload = {
            "name": name,
            "iban": iban,
            "currency": currency,
            "bank_name": bank_name,
            "address": address,
        }

        response = await self.http.post("/beneficiaries", json=payload, user_id=user_id)
        return response.json()

    async def list(self, user_id: str) -> list[dict[str, Any]]:
        """
        List all beneficiaries for a user.

        Args:
            user_id: User ID to list beneficiaries for

        Returns:
            List of beneficiary objects
        """
        response = await self.http.get("/beneficiaries", user_id=user_id)
        return response.json()
