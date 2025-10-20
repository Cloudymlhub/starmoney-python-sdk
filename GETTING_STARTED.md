# StarMoney Python SDK - Getting Started

## 🚀 Installation & Setup

### 1. Install Dependencies

```bash
cd sdk/
poetry install
```

### 2. Configure Credentials

The SDK needs JWT credentials to authenticate with the StarMoney API.

**Option A: Use your existing dev secrets**

Your notebook already has the setup in `.dev_secrets.json`. Extract the JWT secret:

```python
import json

# Load dev secrets
with open('../.dev_secrets.json') as f:
    secrets = json.load(f)

jwt_secrets = json.loads(secrets['jwt_secrets'])
jwt_secret = jwt_secrets['whatsapp-service']  # Or your service name
```

**Option B: Set environment variables**

```bash
export STARMONEY_JWT_SECRET="your-jwt-secret-here"
export STARMONEY_ISSUER="your-service-name"
```

### 3. Run the Quick Start Example

```bash
# Make sure API is running (localhost:8000)
# Terminal 1:
make launch-app

# Terminal 2:
cd sdk/
poetry run python examples/quickstart.py
```

## ✅ Run Integration Tests

Tests replicate your notebook's payment flow:

```bash
# Make sure API is running
cd sdk/
poetry run pytest tests/integration/ -v -s
```

## 📦 Using SDK in Your Project

### Install from Local Path (for development)

```bash
# In your other project
pip install -e /path/to/starmoney-bank-service/sdk/
```

### Use in Your Code

```python
from starmoney import StarmoneyClient

async def send_payment_example():
    async with StarmoneyClient(
        jwt_secret="your-secret",
        issuer="your-service"
    ) as client:
        # Your code here...
        payment = await client.payments.send(...)
```

## 🔍 What's Included

- ✅ **Authentication**: JWT service/user tokens
- ✅ **Accounts**: Create, link rails
- ✅ **Beneficiaries**: Create, list
- ✅ **Payments**: Send, check status (with auto-idempotency)
- ✅ **Webhooks**: Subscribe, validate signatures
- ✅ **Error Handling**: Domain-specific exceptions
- ✅ **Examples**: Quickstart + webhook handler
- ✅ **Tests**: Integration tests against local API

## 📝 Next Steps

1. **Test locally**: Run `examples/quickstart.py`
2. **Adapt for your project**: Copy patterns from examples
3. **Add to your service**: Install SDK in your other project
4. **Deploy together**: Use monorepo or publish to PyPI

## 🐛 Troubleshooting

**"Connection refused"**: Make sure API is running on localhost:8000

```bash
make launch-app
```

**"Invalid JWT"**: Check that jwt_secret matches `.dev_secrets.json`

**"Import error"**: Make sure you ran `poetry install` in `sdk/` directory

## 🎯 Comparison: Notebook vs SDK

| Notebook (Manual) | SDK (Simple) |
|------------------|--------------|
| ~50 lines of setup code | 3 lines to initialize |
| Manual JWT generation | Automatic authentication |
| Raw HTTP requests | Clean async methods |
| Manual error handling | Domain exceptions |
| No type hints | Full IDE autocomplete |

**Notebook approach**:
```python
# Manual JWT
payload = {"iss": issuer, "exp": ..., "iat": ...}
token = jwt.encode(payload, secret, algorithm="HS256")
headers = {"Authorization": f"Bearer {token}"}

# Raw HTTP
response = requests.post(f"{API_URL}/payments", json=data, headers=headers)
payment = response.json()
```

**SDK approach**:
```python
# Clean and simple
payment = await client.payments.send(user_id=user_id, amount=100, ...)
```

Much cleaner! 🎉
