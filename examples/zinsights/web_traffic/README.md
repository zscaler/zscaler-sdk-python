# Web Traffic Examples

Examples for querying web traffic analytics data from Z-Insights.

## Available Methods

| Method | Description |
|--------|-------------|
| `get_traffic_by_location()` | Get web traffic grouped by location |
| `get_traffic_by_user()` | Get web traffic grouped by user |
| `get_protocols()` | Get web traffic protocol distribution |

## Usage

```bash
# Set environment variables
export ZSCALER_CLIENT_ID="your_client_id"
export ZSCALER_CLIENT_SECRET="your_client_secret"
export ZSCALER_VANITY_DOMAIN="your_vanity_domain"
export ZSCALER_CLOUD="beta"

# Run the example
python web_traffic_example.py
```

## Example Output

```
============================================================
Web Traffic by Location
============================================================
Headquarters: 150000 transactions
Branch Office A: 85000 transactions
Branch Office B: 42000 transactions
...
```

