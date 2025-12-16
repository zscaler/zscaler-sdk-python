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
shadow_it_example.py
====================

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

This example demonstrates how to query Shadow IT discovered applications
from Z-Insights using the Zscaler Python SDK.

Usage:
    python shadow_it_example.py [--limit <number>] [--days <number>]

Environment Variables:
    ZSCALER_CLIENT_ID       Your Zscaler OneAPI client ID
    ZSCALER_CLIENT_SECRET   Your Zscaler OneAPI client secret
    ZSCALER_VANITY_DOMAIN   Your Zscaler vanity domain
    ZSCALER_CLOUD           Zscaler cloud (e.g., beta, production)
"""

import argparse
import os
import sys
import time

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


def get_time_range(days: int):
    """Get start and end time in epoch milliseconds.
    
    Note: Z-Insights API requires end_time to be at least 1 day before current time.
    """
    # End time is 1 day ago (API requirement)
    end_time = int(time.time() * 1000) - (1 * 24 * 60 * 60 * 1000)
    # Start time is 'days' days before end_time
    start_time = end_time - (days * 24 * 60 * 60 * 1000)
    return start_time, end_time


def print_header(title: str):
    """Print a formatted header."""
    print("\n" + "=" * 60)
    print(title)
    print("=" * 60)


def format_bytes(bytes_val):
    """Format bytes into human-readable format."""
    if bytes_val is None:
        return "N/A"
    for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
        if bytes_val < 1024:
            return f"{bytes_val:.2f} {unit}"
        bytes_val /= 1024
    return f"{bytes_val:.2f} PB"


def main():
    parser = argparse.ArgumentParser(
        description="Query Shadow IT discovered applications from Z-Insights"
    )
    parser.add_argument(
        "--limit",
        type=int,
        default=10,
        help="Maximum number of entries to return (default: 10)"
    )
    parser.add_argument(
        "--days",
        type=int,
        default=7,
        help="Number of days to query (default: 7)"
    )
    args = parser.parse_args()

    config = get_config()
    start_time, end_time = get_time_range(args.days)

    print(f"Querying Shadow IT data for the last {args.days} days...")

    with ZscalerClient(config) as client:
        # Query discovered applications
        print_header("Shadow IT Discovered Applications")
        entries, response, error = client.zinsights.shadow_it.get_apps(
            start_time=start_time,
            end_time=end_time,
            limit=args.limit
        )

        if error:
            print(f"Error: {error}")
        elif entries:
            print(f"  Found {len(entries)} applications:\n")
            for entry in entries:
                app_name = entry.get('application', 'Unknown')
                category = entry.get('application_category', 'N/A')
                risk = entry.get('risk_index', 'N/A')
                state = entry.get('sanctioned_state', 'N/A')
                integrations = entry.get('integration', 0)
                data_consumed = entry.get('data_consumed', 0)
                print(f"  App: {app_name}")
                print(f"    Category: {category}")
                print(f"    Risk Index: {risk}")
                print(f"    Status: {state}")
                print(f"    Integrations: {integrations}")
                print(f"    Data Consumed: {format_bytes(data_consumed)}")
                print()
        else:
            print("  No Shadow IT applications found.")

        # Query comprehensive summary
        print_header("Shadow IT Summary")
        summary, response, error = client.zinsights.shadow_it.get_shadow_it_summary(
            start_time=start_time,
            end_time=end_time
        )

        if error:
            print(f"Error: {error}")
        elif summary:
            # Top-level statistics
            print(f"  Total Apps: {summary.get('total_apps', 0):,}")
            print(f"  Total Bytes: {format_bytes(summary.get('total_bytes', 0))}")
            print(f"  Upload Bytes: {format_bytes(summary.get('total_upload_bytes', 0))}")
            print(f"  Download Bytes: {format_bytes(summary.get('total_download_bytes', 0))}")
            
            # Sample from group_by_app_cat_for_app
            print("\n  Apps by Category (top 5):")
            group_data = summary.get('group_by_app_cat_for_app', {})
            entries = group_data.get('entries', [])[:5]
            for entry in entries:
                name = entry.get('name', 'Unknown')
                total = entry.get('total', 0)
                print(f"    {name}: {total:,} apps")
        else:
            print("  No summary data available.")

    print("\n" + "=" * 60)
    print("Query completed successfully!")
    print("=" * 60)


if __name__ == "__main__":
    main()
