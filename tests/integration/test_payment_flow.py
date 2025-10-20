"""
StarMoney SDK - Integration Test

Tests the SDK against a live StarMoney API instance (localhost:8000).
Replicates the notebook's payment lifecycle test.
"""

import pytest
import os
from starmoney import StarmoneyClient


@pytest.fixture
async def client():
    """Create SDK client connected to local dev environment."""
    # Load credentials from environment or use dev defaults
    jwt_secret = os.getenv("STARMONEY_JWT_SECRET", "your-dev-jwt-secret")
    issuer = os.getenv("STARMONEY_ISSUER", "test-service")
    
    async with StarmoneyClient(
        jwt_secret=jwt_secret,
        issuer=issuer,
        base_url="http://localhost:8000/api/v1"
    ) as client:
        yield client


@pytest.mark.asyncio
async def test_complete_payment_flow(client: StarmoneyClient):
    """
    Test complete payment lifecycle:
    1. Create account
    2. Link payment rail
    3. Create beneficiary
    4. Send payment
    5. Check payment status
    
    Matches the notebook's success path test.
    """
    # 1. Create account
    account = await client.accounts.create(
        first_name="SDK",
        last_name="Test",
        email="sdk-test@example.com",
        phone_number="+1234567890",
        document_type="PASSPORT",
        document_number="SDK123456",
        address="123 SDK Test St"
    )
    
    assert "user_id" in account
    user_id = account["user_id"]
    print(f"✅ Account created: {user_id}")
    
    # 2. Link payment rail
    rail_result = await client.accounts.link_rail(user_id, rail_name="BDK")
    assert rail_result is not None
    print("✅ Rail linked")
    
    # 3. Create beneficiary
    beneficiary = await client.beneficiaries.create(
        user_id=user_id,
        name="SDK Test Beneficiary",
        iban="FR1420041010050500013M02606",
        currency="EUR",
        bank_name="SDK Test Bank",
        address="456 SDK Test Ave"
    )
    
    assert "iban" in beneficiary
    assert beneficiary["name"] == "SDK Test Beneficiary"
    print(f"✅ Beneficiary created: {beneficiary['name']}")
    
    # 4. Send payment
    payment = await client.payments.send(
        user_id=user_id,
        amount=100.00,
        currency="EUR",
        beneficiary_iban=beneficiary["iban"],
        beneficiary_name=beneficiary["name"],
        description="SDK integration test payment"
    )
    
    assert "transaction_id" in payment
    assert "client_transaction_id" in payment
    assert payment["amount"] == "100.00"
    assert payment["currency"] == "EUR"
    
    client_txn_id = payment["client_transaction_id"]
    print(f"✅ Payment sent: {client_txn_id}")
    
    # 5. Check payment status
    status = await client.payments.get_status(
        user_id=user_id,
        client_transaction_id=client_txn_id
    )
    
    assert "status" in status
    assert status["status"] in ["PENDING", "PROCESSING", "ACCEPTED", "COMPLETED", "FAILED"]
    assert status["amount"] == "100.00"
    assert status["currency"] == "EUR"
    
    print(f"✅ Payment status: {status['status']}")
    print("\n🎉 Complete payment flow test PASSED!")


@pytest.mark.asyncio
async def test_idempotency(client: StarmoneyClient):
    """Test that duplicate payments are prevented via client_transaction_id."""
    # Create account and link rail
    account = await client.accounts.create(
        first_name="Idempotency",
        last_name="Test",
        email="idempotency@example.com",
        phone_number="+1987654321",
        document_type="PASSPORT",
        document_number="IDEM123",
        address="123 Idem St"
    )
    user_id = account["user_id"]
    await client.accounts.link_rail(user_id)
    
    # Send payment with custom client_transaction_id
    custom_id = "test-idempotency-12345"
    
    payment1 = await client.payments.send(
        user_id=user_id,
        amount=50.00,
        currency="EUR",
        beneficiary_iban="FR1420041010050500013M02606",
        beneficiary_name="Test",
        description="Idempotency test",
        client_transaction_id=custom_id
    )
    
    assert payment1["client_transaction_id"] == custom_id
    
    # Try to send again with same client_transaction_id (should be idempotent)
    from starmoney import DuplicateResourceError
    
    with pytest.raises(DuplicateResourceError):
        await client.payments.send(
            user_id=user_id,
            amount=50.00,
            currency="EUR",
            beneficiary_iban="FR1420041010050500013M02606",
            beneficiary_name="Test",
            description="Duplicate payment",
            client_transaction_id=custom_id  # Same ID
        )
    
    print("✅ Idempotency test PASSED - duplicate prevented")


@pytest.mark.asyncio
async def test_webhook_subscription(client: StarmoneyClient):
    """Test webhook subscription creation."""
    result = await client.webhooks.batch_subscribe(
        endpoint_url="http://localhost:8001/webhook",
        webhook_secret="test-webhook-secret-sdk",
        event_subscriptions=[
            {"event_type": "payment.initiated", "subscribed_users": None},
            {"event_type": "payment.completed", "subscribed_users": None},
            {"event_type": "payment.failed", "subscribed_users": None},
        ],
        retry_attempts=3,
        timeout_seconds=10
    )
    
    assert "total_created" in result
    assert result["total_created"] == 3
    
    print(f"✅ Webhook subscription test PASSED - {result['total_created']} events subscribed")


if __name__ == "__main__":
    # Run tests with pytest
    pytest.main([__file__, "-v", "-s"])
