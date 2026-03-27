# SaaS Security (CASB) Examples

Examples for querying Cloud Access Security Broker (CASB) data from Z-Insights.

## Available Methods

| Method | Description |
|--------|-------------|
| `get_casb_app_report()` | Get CASB application report data |
| `get_casb_incidents()` | Get CASB incidents (DLP or malware) |

## Usage

```bash
# Set environment variables
export ZSCALER_CLIENT_ID="your_client_id"
export ZSCALER_CLIENT_SECRET="your_client_secret"
export ZSCALER_VANITY_DOMAIN="your_vanity_domain"
export ZSCALER_CLOUD="beta"

# Run the example
python saas_security_example.py
```

