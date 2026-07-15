# ZDX List Applications

This example demonstrates how to retrieve a list of all active applications configured within the ZDX tenant using both the OneAPI client and Legacy client.

## Prerequisites

### For OneAPI Client (Default)
Set the following environment variables:
```bash
export ZSCALER_CLIENT_ID="your_client_id"
export ZSCALER_CLIENT_SECRET="your_client_secret"
export ZSCALER_VANITY_DOMAIN="your_vanity_domain"  # Optional
```

### For Legacy Client
Set the following environment variables:
```bash
export ZDX_CLIENT_ID="your_zdx_client_id"
export ZDX_CLIENT_SECRET="your_zdx_client_secret"
```

## Usage

### Basic Usage

Run the script and follow the interactive prompts:
```bash
python zdx_list_apps.py
```

### Using Legacy Client

To use the legacy ZDX client instead of the OneAPI client, add the `--use-legacy-client` flag:
```bash
python zdx_list_apps.py --use-legacy-client
```

## Interactive Prompts

The script will prompt you for the following information:

### Optional Inputs
- **Hours to look back**: Number of hours to look back for data (optional)
- **Location ID**: Specific location ID to filter by (optional)
- **Department ID**: Specific department ID to filter by (optional)
- **Geolocation ID**: Specific geolocation ID to filter by (optional)

## Output Format

The script displays applications in a formatted table with the following columns:
- **App ID**: The unique identifier for the application
- **App Name**: The name of the application
- **Score**: The current application score (typically 0-100)
- **Most Impacted Region**: The region with the most performance issues
- **Total Users**: The total number of users for this application

## Examples

### OneAPI Client Examples

```bash
# Run with OneAPI client (default)
python zdx_list_apps.py

# The script will prompt for:
# 1. Hours to look back (optional)
# 2. Location ID (optional)
# 3. Department ID (optional)
# 4. Geolocation ID (optional)
```

### Legacy Client Examples

```bash
# Run with legacy client
python zdx_list_apps.py --use-legacy-client

# Same interactive prompts as OneAPI client
```

## Sample Output

```
+--------+------------------+-------+----------------------+------------+
| App ID |     App Name     | Score | Most Impacted Region| Total Users|
+--------+------------------+-------+----------------------+------------+
|   123  |   Salesforce    |  85.2 |       United States  |     150    |
|   124  |   Microsoft 365 |  92.1 |       United Kingdom |     200    |
|   125  |   Google Workspace|  78.5 |       Canada        |      75    |
+--------+------------------+-------+----------------------+------------+
```

## Error Handling

The script includes comprehensive error handling:
- Validates required environment variables
- Handles API errors gracefully
- Provides clear error messages for missing credentials
- Supports both client types with appropriate error messages
- Handles invalid user input for time filters

## Notes

- The OneAPI client is the default and recommended approach
- The legacy client is provided for backward compatibility
- Both clients return the same data structure for consistent display
- The `--use-legacy-client` flag switches between client types without changing the output format
- All API calls include proper error handling with tuple returns
- The script handles both object types (with `as_dict()` method) and dictionary types
- Application scores are typically measured on a scale of 0-100, where higher scores indicate better performance
- The "Most Impacted Region" field shows the country with the most performance issues for that application 