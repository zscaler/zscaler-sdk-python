# Z-Insights Examples

This directory contains example scripts demonstrating how to use the Z-Insights GraphQL API through the Zscaler Python SDK.

## Overview

Z-Insights provides analytics and reporting data via GraphQL for:

- **Web Traffic** - Traffic by location, user, protocols, threat categories
- **SaaS Security (CASB)** - Cloud Access Security Broker data and incidents
- **Cyber Security** - Cybersecurity incident data and threat intelligence
- **Zero Trust Firewall** - Firewall traffic analytics by action, location, network services
- **IoT Device Visibility** - IoT device statistics and classification
- **Shadow IT Discovery** - Unsanctioned application discovery and risk assessment

## Prerequisites

Before running these examples, ensure you have:

1. **Zscaler OneAPI Credentials**:
   - Client ID
   - Client Secret
   - Vanity Domain

2. **Environment Variables** (recommended):
   ```bash
   export ZSCALER_CLIENT_ID="your_client_id"
   export ZSCALER_CLIENT_SECRET="your_client_secret"
   export ZSCALER_VANITY_DOMAIN="your_vanity_domain"
   export ZSCALER_CLOUD="beta"  # or "production", "zscalerthree", etc.
   ```

3. **Python SDK installed**:
   ```bash
   pip install zscaler-sdk-python
   ```

## Examples

| Example | Description |
|---------|-------------|
| [web_traffic_example.py](web_traffic/web_traffic_example.py) | Query web traffic data by location and user |
| [saas_security_example.py](saas_security/saas_security_example.py) | Query CASB application reports and incidents |
| [cyber_security_example.py](cyber_security/cyber_security_example.py) | Query cybersecurity incident data |
| [firewall_example.py](firewall/firewall_example.py) | Query Zero Trust Firewall analytics |
| [iot_example.py](iot/iot_example.py) | Query IoT device statistics |
| [shadow_it_example.py](shadow_it/shadow_it_example.py) | Query Shadow IT discovered applications |

## Authentication

Z-Insights uses OneAPI OAuth2.0 authentication. Legacy API keys are **not supported**.

```python
from zscaler import ZscalerClient

config = {
    'clientId': 'your_client_id',
    'clientSecret': 'your_client_secret',
    'vanityDomain': 'your_vanity_domain',
    'cloud': 'beta',
}

with ZscalerClient(config) as client:
    # Access Z-Insights APIs
    entries, response, error = client.zinsights.web_traffic.get_traffic_by_location(...)
```

## Time Parameters

Z-Insights queries use epoch milliseconds for time parameters:

```python
import time

# Current time in milliseconds
end_time = int(time.time() * 1000)

# 7 days ago
start_time = end_time - (7 * 24 * 60 * 60 * 1000)
```

## Response Format

All Z-Insights methods return a tuple of `(data, response, error)`:

```python
entries, response, error = client.zinsights.web_traffic.get_traffic_by_location(
    start_time=start_time,
    end_time=end_time,
    limit=10
)

if error:
    print(f"Error: {error}")
else:
    for entry in entries:
        print(f"{entry['name']}: {entry['total']}")
```

