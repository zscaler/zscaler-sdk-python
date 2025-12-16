# Zero Trust Firewall Examples

Examples for querying Zero Trust Firewall analytics from Z-Insights.

## Available Methods

| Method | Description |
|--------|-------------|
| `get_traffic_by_action()` | Get firewall traffic grouped by action (allow/block) |
| `get_traffic_by_location()` | Get firewall traffic grouped by location |
| `get_network_services()` | Get firewall network services data |

## Usage

```bash
# Set environment variables
export ZSCALER_CLIENT_ID="your_client_id"
export ZSCALER_CLIENT_SECRET="your_client_secret"
export ZSCALER_VANITY_DOMAIN="your_vanity_domain"
export ZSCALER_CLOUD="beta"

# Run the example
python firewall_example.py
```

