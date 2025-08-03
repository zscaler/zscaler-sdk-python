# ZDX Application Score

This example demonstrates how to retrieve application scores for Zscaler Digital Experience (ZDX) using both the OneAPI client and Legacy client.

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
python zdx_app_score.py
```

### Using Legacy Client

To use the legacy ZDX client instead of the OneAPI client, add the `--use-legacy-client` flag:
```bash
python zdx_app_score.py --use-legacy-client
```

## Interactive Prompts

The script will prompt you for the following information:

### Required Inputs
- **Application ID**: The unique identifier for the application you want to retrieve scores for

### Optional Inputs
- **Hours to look back**: Number of hours to look back for data (optional)
- **Location ID**: Specific location ID to filter by (optional)
- **Department ID**: Specific department ID to filter by (optional)
- **Geolocation ID**: Specific geolocation ID to filter by (optional)

## Output Format

The script displays application scores in a formatted table with the following columns:
- **Metric**: The metric being measured (default: "score")
- **Unit**: The unit of measurement
- **Timestamp**: When the measurement was taken
- **Value**: The actual score value

## Examples

### OneAPI Client Examples

```bash
# Run with OneAPI client (default)
python zdx_app_score.py

# The script will prompt for:
# 1. Application ID
# 2. Hours to look back (optional)
# 3. Location ID (optional)
# 4. Department ID (optional)
# 5. Geolocation ID (optional)
```

### Legacy Client Examples

```bash
# Run with legacy client
python zdx_app_score.py --use-legacy-client

# Same interactive prompts as OneAPI client
```

## Sample Output

```
+-------+------+---------------------+-------+
| Metric| Unit |      Timestamp      | Value |
+-------+------+---------------------+-------+
| score |      | 2024-01-15 10:30:00|  85.2 |
| score |      | 2024-01-15 11:30:00|  87.1 |
| score |      | 2024-01-15 12:30:00|  86.5 |
+-------+------+---------------------+-------+
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