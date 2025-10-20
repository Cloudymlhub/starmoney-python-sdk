"""StarMoney SDK - Webhooks Resource"""

from typing import Any, Optional
from ..http_client import HTTPClient


class WebhooksResource:
    """
    Webhooks resource for managing event subscriptions.

    Handles:
    - Creating webhook subscriptions
    - Batch subscribing to multiple events
    """

    def __init__(self, http_client: HTTPClient):
        self.http = http_client

    async def batch_subscribe(
        self,
        endpoint_url: str,
        webhook_secret: str,
        event_subscriptions: list[dict[str, Any]],
        retry_attempts: int = 3,
        timeout_seconds: int = 10,
    ) -> dict[str, Any]:
        """
        Subscribe to multiple webhook events in one request.

        Args:
            endpoint_url: URL where webhooks will be delivered
            webhook_secret: Secret for HMAC signature validation
            event_subscriptions: List of event subscriptions
            retry_attempts: Number of retry attempts for failed deliveries
            timeout_seconds: Webhook delivery timeout

        Returns:
            Subscription confirmation data

        Example:
            ```python
            result = await client.webhooks.batch_subscribe(
                endpoint_url="https://yourapp.com/webhooks",
                webhook_secret="your-webhook-secret",
                event_subscriptions=[
                    {"event_type": "payment.initiated", "subscribed_users": None},
                    {"event_type": "payment.completed", "subscribed_users": None},
                    {"event_type": "payment.failed", "subscribed_users": None},
                ],
                retry_attempts=3,
                timeout_seconds=10
            )

            print(f"Subscribed to {result['total_created']} events")
            ```
        """
        payload = {
            "endpoint_url": endpoint_url,
            "webhook_secret": webhook_secret,
            "event_subscriptions": event_subscriptions,
            "retry_attempts": retry_attempts,
            "timeout_seconds": timeout_seconds,
        }

        response = await self.http.post("/webhook-subscriptions/batch", json=payload)
        return response.json()

    async def create_subscription(
        self,
        endpoint_url: str,
        webhook_secret: str,
        event_type: str,
        subscribed_users: Optional[list[str]] = None,
        retry_attempts: int = 3,
        timeout_seconds: int = 10,
    ) -> dict[str, Any]:
        """
        Subscribe to a single webhook event.

        Args:
            endpoint_url: URL where webhooks will be delivered
            webhook_secret: Secret for HMAC signature validation
            event_type: Event type to subscribe to (e.g., 'payment.completed')
            subscribed_users: Optional list of user IDs to filter events
            retry_attempts: Number of retry attempts for failed deliveries
            timeout_seconds: Webhook delivery timeout

        Returns:
            Subscription data
        """
        payload = {
            "endpoint_url": endpoint_url,
            "webhook_secret": webhook_secret,
            "event_type": event_type,
            "subscribed_users": subscribed_users,
            "retry_attempts": retry_attempts,
            "timeout_seconds": timeout_seconds,
        }

        response = await self.http.post("/webhook-subscriptions", json=payload)
        return response.json()
