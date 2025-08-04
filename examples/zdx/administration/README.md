# ZDX Administration Management

This example demonstrates how to manage Departments and Locations for Zscaler Digital Experience (ZDX) using both the OneAPI client and Legacy client.

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

### Basic Commands

List all departments:
```bash
python zdx_management.py -d
```

List all locations:
```bash
python zdx_management.py -l
```

### Using Legacy Client

To use the legacy ZDX client instead of the OneAPI client, add the `--use-legacy-client` flag:

```bash
# List departments using legacy client
python zdx_management.py -d --use-legacy-client

# List locations using legacy client
python zdx_management.py -l --use-legacy-client
```

### Advanced Options

Search for departments/locations from the past N hours:
```bash
# List departments from the past 5 hours
python zdx_management.py -d -s 5

# List locations from the past 10 hours using legacy client
python zdx_management.py -l -s 10 --use-legacy-client
```

### Verbose Output

Enable verbose logging:
```bash
python zdx_management.py -d -v
python zdx_management.py -d -vv  # Extra verbose
```

### Quiet Mode

Suppress all output except errors:
```bash
python zdx_management.py -d -q
```

## Command Line Arguments

- `-d, --departments`: List all departments
- `-l, --locations`: List all locations
- `-s, --since`: Specify how many hours back to search (optional)
- `--use-legacy-client`: Use legacy ZDX client instead of OneAPI client
- `-v, --verbose`: Verbose output (-vv for extra verbose)
- `-q, --quiet`: Suppress all output
- `-h, --help`: Show help message

## Examples

### OneAPI Client Examples

```bash
# List all departments
python zdx_management.py -d

# List all locations
python zdx_management.py -l

# List departments from the past 3 hours
python zdx_management.py -d -s 3

# List locations with verbose output
python zdx_management.py -l -v
```

### Legacy Client Examples

```bash
# List all departments using legacy client
python zdx_management.py -d --use-legacy-client

# List all locations using legacy client
python zdx_management.py -l --use-legacy-client

# List departments from the past 5 hours using legacy client
python zdx_management.py -d -s 5 --use-legacy-client
```

## Output Format

The script displays results in a formatted table with the following columns:
- **ID**: The unique identifier for the department or location
- **Name**: The name of the department or location

## Error Handling

The script includes comprehensive error handling:
- Validates required environment variables
- Handles API errors gracefully
- Provides clear error messages for missing credentials
- Supports both client types with appropriate error messages

## Notes

- The OneAPI client is the default and recommended approach
- The legacy client is provided for backward compatibility
- Both clients return the same data structure for consistent display
- The `--use-legacy-client` flag switches between client types without changing the output format
