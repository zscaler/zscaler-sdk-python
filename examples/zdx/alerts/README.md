# ZDX Alerts Management

This example demonstrates how to manage alerts for Zscaler Digital Experience (ZDX) using both the OneAPI client and Legacy client.

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
python zdx_alerts_management.py
```

### Using Legacy Client

To use the legacy ZDX client instead of the OneAPI client, add the `--use-legacy-client` flag:
```bash
python zdx_alerts_management.py --use-legacy-client
```

## Interactive Menu Options

The script provides an interactive menu with the following options:

### a. Retrieve All Ongoing Alerts
- Retrieves all ongoing alerts with optional time filters
- Defaults to the previous 2 hours if no time is specified
- Displays alert details in a formatted table

### b. Retrieve Historical Alerts
- Retrieves historical alerts with optional time filters
- Defaults to the previous 2 hours if no time is specified
- Displays alert details in a formatted table

### c. Retrieve Alert Details
- Retrieves detailed information for a specific alert ID
- Shows impacted departments, locations, and geolocations
- Displays comprehensive alert information

### d. Retrieve Affected Devices
- Retrieves devices affected by a specific alert ID
- Shows device and user information
- Includes optional time filtering

## Time Filtering

When prompted for the number of hours to look back:
- Enter a number (e.g., `5` for 5 hours)
- Press Enter to use the default (2 hours)
- The time filter applies to ongoing alerts, historical alerts, and affected devices

## Output Format

### Alert Table
The script displays alerts in a formatted table with the following columns:
- **ID**: Alert identifier
- **Rule Name**: Name of the alert rule
- **Severity**: Alert severity level
- **Alert Type**: Type of alert
- **Status**: Current alert status
- **Num Geolocations**: Number of affected geolocations
- **Num Devices**: Number of affected devices
- **Started On**: When the alert started
- **Ended On**: When the alert ended (N/A if ongoing)

### Device Table
For affected devices, the table includes:
- **Device ID**: Unique device identifier
- **Device Name**: Name of the device
- **User ID**: User identifier
- **User Name**: Name of the user
- **User Email**: User's email address

### Department/Location Tables
For alert details, additional tables show:
- **Name**: Department or location name
- **Num Devices**: Number of devices in that department/location

## Examples

### OneAPI Client Examples

```bash
# Run with OneAPI client (default)
python zdx_alerts_management.py

# The script will prompt for:
# 1. Alert type (a/b/c/d)
# 2. Time filter (if applicable)
# 3. Alert ID (for options c and d)
```

### Legacy Client Examples

```bash
# Run with legacy client
python zdx_alerts_management.py --use-legacy-client

# Same interactive prompts as OneAPI client
```

## Error Handling

The script includes comprehensive error handling:
- Validates required environment variables
- Handles API errors gracefully
- Provides clear error messages for missing credentials
- Supports both client types with appropriate error messages
- Handles invalid user input for time filters

## Debugging

The script includes debug print statements to help troubleshoot:
- Shows data collected from API calls
- Displays processing information for each alert
- Helps identify data structure issues

## Notes

- The OneAPI client is the default and recommended approach
- The legacy client is provided for backward compatibility
- Both clients return the same data structure for consistent display
- The `--use-legacy-client` flag switches between client types without changing the output format
- All API calls include proper error handling with tuple returns
- The script handles both object types (with `as_dict()` method) and dictionary types
