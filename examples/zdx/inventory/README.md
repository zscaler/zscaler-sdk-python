# ZDX Software Inventory Management

This example demonstrates how to manage software inventory for Zscaler Digital Experience (ZDX) using both the OneAPI client and Legacy client.

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
python zdx_software_management.py
```

### Using Legacy Client

To use the legacy ZDX client instead of the OneAPI client, add the `--use-legacy-client` flag:
```bash
python zdx_software_management.py --use-legacy-client
```

## Interactive Menu Options

The script provides an interactive menu with the following options:

### a. Retrieve All Software
- Retrieves all software with optional time filters
- Defaults to the previous 2 hours if no time is specified
- Displays software details in a formatted table
- Shows software key, name, vendor, group, install type, and usage statistics

### b. Retrieve Software Details for Specific Software Key
- Retrieves detailed information for a specific software key
- Shows installation details including version, OS, user, device, and install date
- Includes optional time filtering

## Interactive Prompts

The script will prompt you for the following information:

### Required Inputs
- **Choice**: Select option 'a' or 'b'
- **Software Key**: For option 'b', enter the specific software key to search for

### Optional Inputs
- **Hours to look back**: Number of hours to look back for data (defaults to 2 hours)
- **Number of entries**: Maximum number of entries to display (optional, defaults to all)

## Output Format

### Software List Table
The script displays software in a formatted table with the following columns:
- **Software Key**: Unique identifier for the software
- **Software Name**: Name of the software
- **Vendor**: Software vendor
- **Software Group**: Group classification
- **Install Type**: Type of installation
- **User Total**: Total number of users
- **Device Total**: Total number of devices

### Software Details Table
For specific software keys, the table includes:
- **Software Key**: Unique identifier
- **Software Name**: Name of the software
- **Version**: Software version
- **Software Group**: Group classification
- **OS**: Operating system
- **Vendor**: Software vendor
- **User ID**: User identifier
- **Device ID**: Device identifier
- **Hostname**: Device hostname
- **Username**: User name
- **Install Date**: When the software was installed

## Examples

### OneAPI Client Examples

```bash
# Run with OneAPI client (default)
python zdx_software_management.py

# The script will prompt for:
# 1. Software option (a/b)
# 2. Number of entries to display (optional)
# 3. Hours to look back (optional)
# 4. Software key (for option b)
```

### Legacy Client Examples

```bash
# Run with legacy client
python zdx_software_management.py --use-legacy-client

# Same interactive prompts as OneAPI client
```

## Sample Output

### Software List
```
+-------------+------------------+--------+------------------+------------+-----------+-------------+
| Software Key|   Software Name  | Vendor |  Software Group  | Install Type| User Total| Device Total|
+-------------+------------------+--------+------------------+------------+-----------+-------------+
| chrome      |   Google Chrome  | Google |     Browser      |    MSI     |    150    |     120     |
| office365   | Microsoft Office |Microsoft| Productivity Suite|   Cloud    |    200    |     180     |
+-------------+------------------+--------+------------------+------------+-----------+-------------+
```

### Software Details
```
+-------------+------------------+---------+------------------+--------+--------+--------+----------+----------+----------+---------------------+
| Software Key|   Software Name  | Version |  Software Group  |   OS   | Vendor | User ID| Device ID| Hostname | Username |    Install Date     |
+-------------+------------------+---------+------------------+--------+--------+--------+----------+----------+----------+---------------------+
| chrome      |   Google Chrome  |  120.0  |     Browser      | Windows| Google |  12345 |   67890  | PC-001   | john.doe| 2024-01-15 10:30:00|
+-------------+------------------+---------+------------------+--------+--------+--------+----------+----------+----------+---------------------+
```

## Error Handling

The script includes comprehensive error handling:
- Validates required environment variables
- Handles API errors gracefully
- Provides clear error messages for missing credentials
- Supports both client types with appropriate error messages
- Handles invalid user input for time filters and entry limits

## Debugging

The script includes debug print statements to help troubleshoot:
- Shows data collected from API calls
- Displays processing information for each software item
- Helps identify data structure issues

## Notes

- The OneAPI client is the default and recommended approach
- The legacy client is provided for backward compatibility
- Both clients return the same data structure for consistent display
- The `--use-legacy-client` flag switches between client types without changing the output format
- All API calls include proper error handling with tuple returns
- The script handles both object types (with `as_dict()` method) and dictionary types
- Software inventory data helps track software usage across the organization
- Install dates are converted from Unix timestamps to human-readable format 