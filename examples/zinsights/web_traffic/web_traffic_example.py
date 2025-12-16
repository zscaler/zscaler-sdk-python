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
web_traffic_example.py
======================

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

This example demonstrates how to query web traffic analytics data from
Z-Insights using the Zscaler Python SDK.

Usage:
    python web_traffic_example.py [--limit <number>] [--days <number>]

Options:
    --limit     Maximum number of entries to return (default: 10)
    --days      Number of days to query (default: 7)

Examples:
    # Get top 10 locations by traffic for the last 7 days
    python web_traffic_example.py

    # Get top 20 locations by traffic for the last 30 days
    python web_traffic_example.py --limit 20 --days 30

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


def main():
    parser = argparse.ArgumentParser(
        description="Query web traffic analytics from Z-Insights"
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

    print(f"Querying web traffic for the last {args.days} days...")

    with ZscalerClient(config) as client:
        # Query traffic by location
        print_header("Web Traffic by Location")
        entries, response, error = client.zinsights.web_traffic.get_traffic_by_location(
            start_time=start_time,
            end_time=end_time,
            traffic_unit="TRANSACTIONS",
            limit=args.limit
        )

        if error:
            print(f"Error: {error}")
        elif entries:
            for entry in entries:
                print(f"  {entry.get('name', 'Unknown')}: {entry.get('total', 0):,} transactions")
        else:
            print("  No data available for the specified time range.")

        # Query overall traffic (no grouping)
        print_header("Overall Web Traffic (No Grouping)")
        entries, response, error = client.zinsights.web_traffic.get_no_grouping(
            start_time=start_time,
            end_time=end_time,
            traffic_unit="TRANSACTIONS",
            limit=args.limit
        )

        if error:
            print(f"Error: {error}")
        elif entries:
            for entry in entries:
                print(f"  {entry.get('name', 'Unknown')}: {entry.get('total', 0):,} transactions")
        else:
            print("  No data available for the specified time range.")

        # Query protocols
        print_header("Web Traffic by Protocol")
        entries, response, error = client.zinsights.web_traffic.get_protocols(
            start_time=start_time,
            end_time=end_time,
            traffic_unit="TRANSACTIONS",
            limit=args.limit
        )

        if error:
            print(f"Error: {error}")
        elif entries:
            for entry in entries:
                print(f"  {entry.get('name', 'Unknown')}: {entry.get('total', 0):,} transactions")
        else:
            print("  No data available for the specified time range.")

        # Query threat super categories
        print_header("Web Traffic by Threat Super Category")
        entries, response, error = client.zinsights.web_traffic.get_threat_super_categories(
            start_time=start_time,
            end_time=end_time,
            traffic_unit="TRANSACTIONS",
            limit=args.limit
        )

        if error:
            print(f"Error: {error}")
        elif entries:
            for entry in entries:
                print(f"  {entry.get('name', 'Unknown')}: {entry.get('total', 0):,} transactions")
        else:
            print("  No data available for the specified time range.")

        # Query threat class
        print_header("Web Traffic by Threat Class")
        entries, response, error = client.zinsights.web_traffic.get_threat_class(
            start_time=start_time,
            end_time=end_time,
            traffic_unit="TRANSACTIONS",
            limit=args.limit
        )

        if error:
            print(f"Error: {error}")
        elif entries:
            for entry in entries:
                print(f"  {entry.get('name', 'Unknown')}: {entry.get('total', 0):,} transactions")
        else:
            print("  No data available for the specified time range.")

    print("\n" + "=" * 60)
    print("Query completed successfully!")
    print("=" * 60)


if __name__ == "__main__":
    main()
