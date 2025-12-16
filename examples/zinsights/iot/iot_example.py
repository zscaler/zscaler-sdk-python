#!/usr/bin/env python

# Copyright (c) 2023, Zscaler Inc.
#
# Permission to use, copy, modify, and/or distribute this software for any
# purpose with or without fee is hereby granted, provided that the above
# copyright notice and this permission notice appear in all copies.
#
# THE SOFTWARE IS PROVIDED "AS IS" AND THE AUTHOR DISCLAIMS ALL WARRANTIES
# WITH REGARD TO THIS SOFTWARE INCLUDING ALL IMPLIED WARRANTIES OF
# MERCHANTABILITY AND FITNESS. IN NO EVENT SHALL THE AUTHOR BE LIABLE FOR
# ANY SPECIAL, DIRECT, INDIRECT, OR CONSEQUENTIAL DAMAGES OR ANY DAMAGES
# WHATSOEVER RESULTING FROM LOSS OF USE, DATA OR PROFITS, WHETHER IN AN
# ACTION OF CONTRACT, NEGLIGENCE OR OTHER TORTIOUS ACTION, ARISING OUT OF
# OR IN CONNECTION WITH THE USE OR PERFORMANCE OF THIS SOFTWARE.

r"""
iot_example.py
==============

 ________              _
|__  /___| ___ __ _| | ___ _ __
  / // __|/ __/ _` | |/ _ \ '__|
 / /_\__ \ (_| (_| | |  __/ |
/____|___/\___\__,_|_|\___|_|    Python SDK

 _____     ___           _       _     _
|__  /    |_ _|_ __  ___(_) __ _| |__ | |_ ___
  / /_____ | || '_ \/ __| |/ _` | '_ \| __/ __|
 / /_|_____|| || | | \__ \ | (_| | | | | |_\__ \
/____|     |___|_| |_|___/_|\__, |_| |_|\__|___/
                            |___/

This example demonstrates how to query IoT device statistics from
Z-Insights using the Zscaler Python SDK.

Usage:
    python iot_example.py [--limit <number>]

Environment Variables:
    ZSCALER_CLIENT_ID       Your Zscaler OneAPI client ID
    ZSCALER_CLIENT_SECRET   Your Zscaler OneAPI client secret
    ZSCALER_VANITY_DOMAIN   Your Zscaler vanity domain
    ZSCALER_CLOUD           Zscaler cloud (e.g., beta, production)
"""

import argparse
import os
import sys

from zscaler import ZscalerClient


def get_config():
    """Build configuration from environment variables."""
    client_id = os.getenv("ZSCALER_CLIENT_ID")
    client_secret = os.getenv("ZSCALER_CLIENT_SECRET")
    vanity_domain = os.getenv("ZSCALER_VANITY_DOMAIN")
    cloud = os.getenv("ZSCALER_CLOUD", "beta")

    if not all([client_id, client_secret, vanity_domain]):
        print("Error: Missing required environment variables.")
        print("Please set ZSCALER_CLIENT_ID, ZSCALER_CLIENT_SECRET, and ZSCALER_VANITY_DOMAIN")
        sys.exit(1)

    return {
        'clientId': client_id,
        'clientSecret': client_secret,
        'vanityDomain': vanity_domain,
        'cloud': cloud,
    }


def print_header(title: str):
    """Print a formatted header."""
    print("\n" + "=" * 60)
    print(title)
    print("=" * 60)


def main():
    parser = argparse.ArgumentParser(
        description="Query IoT device statistics from Z-Insights"
    )
    parser.add_argument(
        "--limit",
        type=int,
        default=20,
        help="Maximum number of entries to return (default: 20)"
    )
    args = parser.parse_args()

    config = get_config()

    print("Querying IoT device statistics...")

    with ZscalerClient(config) as client:
        print_header("IoT Device Statistics")
        entries, response, error = client.zinsights.iot.get_device_stats(
            limit=args.limit
        )

        if error:
            print(f"Error: {error}")
        elif entries:
            # Group by category for better display
            categories = {}
            for entry in entries:
                category = entry.get('category', 'Unknown')
                if category not in categories:
                    categories[category] = []
                categories[category].append(entry)

            for category, devices in categories.items():
                print(f"\n  {category}:")
                for device in devices:
                    device_type = device.get('type', 'Unknown')
                    count = device.get('device_count', 0)
                    print(f"    - {device_type}: {count:,} devices")
        else:
            print("  No IoT device data available.")

    print("\n" + "=" * 60)
    print("Query completed successfully!")
    print("=" * 60)


if __name__ == "__main__":
    main()

