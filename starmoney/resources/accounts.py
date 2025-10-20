"""StarMoney SDK - Accounts Resource"""

from typing import Any
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
