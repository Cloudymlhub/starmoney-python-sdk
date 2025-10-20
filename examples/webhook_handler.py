"""
StarMoney SDK - Webhook Handler Example

Demonstrates how to receive and validate webhooks from StarMoney API.
Works with FastAPI (can be adapted for Flask or other frameworks).
"""

from fastapi import FastAPI, Request, HTTPException
from starmoney.webhooks import WebhookValidator

app = FastAPI()

# Initialize webhook validator with your secret
# (same secret used when creating webhook subscription)
webhook_validator = WebhookValidator(webhook_secret="your-webhook-secret-here")


@app.post("/webhooks/starmoney")
async def handle_starmoney_webhook(request: Request):
    """
    Receive and validate webhooks from StarMoney API.
    
    CRITICAL: Always validate signatures to prevent spoofed webhooks!
    """
    # Get raw payload bytes
    payload = await request.body()
    
    # Get signature from header
    signature = request.headers.get("X-Webhook-Signature")
    if not signature:
        raise HTTPException(status_code=400, detail="Missing signature header")
    
    # Validate signature and parse webhook
    try:
        event = webhook_validator.parse_webhook(payload, signature)
    except Exception as e:
        # Log security incident
        print(f"⚠️  Invalid webhook signature: {e}")
        raise HTTPException(status_code=401, detail="Invalid signature")
    
    # Process webhook based on event type
    event_type = event.get("event_type")
    event_data = event.get("data", {})
    
    print(f"📨 Received webhook: {event_type}")
    
    if event_type == "payment.initiated":
        handle_payment_initiated(event_data)
    elif event_type == "payment.completed":
        handle_payment_completed(event_data)
    elif event_type == "payment.failed":
        handle_payment_failed(event_data)
    else:
        print(f"⚠️  Unknown event type: {event_type}")
    
    # Always return 200 to acknowledge receipt
    return {"status": "received"}


def handle_payment_initiated(data: dict):
    """Handle payment.initiated event."""
    transaction_id = data.get("transaction_id")
    amount = data.get("amount")
    currency = data.get("currency")
    
    print(f"💰 Payment initiated: {amount} {currency}")
    print(f"   Transaction: {transaction_id}")
    
    # Your business logic here
    # - Update database
    # - Send confirmation email
    # - etc.


def handle_payment_completed(data: dict):
    """Handle payment.completed event."""
    transaction_id = data.get("transaction_id")
    amount = data.get("amount")
    currency = data.get("currency")
    
    print(f"✅ Payment completed: {amount} {currency}")
    print(f"   Transaction: {transaction_id}")
    
    # Your business logic here
    # - Mark order as paid
    # - Trigger fulfillment
    # - Send receipt
    # - etc.


def handle_payment_failed(data: dict):
    """Handle payment.failed event."""
    transaction_id = data.get("transaction_id")
    error = data.get("error", "Unknown error")
    
    print(f"❌ Payment failed: {error}")
    print(f"   Transaction: {transaction_id}")
    
    # Your business logic here
    # - Notify user of failure
    # - Retry logic
    # - Refund if applicable
    # - etc.


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8001)
