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

"""
zdx_management.py
=================

Manage Departments and Locations for Zscaler Digital Experience (ZDX).

**Usage**::

    zdx_management.py [-h] [-v] [-q] [-d] [-l] [-s HOURS] [--use-legacy-client]

**Examples**:

List all Departments:
    $ python zdx_management.py -d

List all Locations:
    $ python zdx_management.py -l

List Departments for the past 5 hours:
    $ python zdx_management.py -d -s 5

Using Legacy Client:
    $ python zdx_management.py -d --use-legacy-client

"""

import argparse
import logging
import json
import os
from prettytable import PrettyTable
from zscaler import ZscalerClient
from zscaler.oneapi_client import LegacyZDXClient


def main():
    parser = argparse.ArgumentParser(description="Manage Departments and Locations for Zscaler Digital Experience (ZDX)")
    parser.add_argument("-v", "--verbose", action="count", help="Verbose (-vv for extra verbose)")
    parser.add_argument("-q", "--quiet", action="store_true", help="Suppress all output")
    parser.add_argument("-d", "--departments", action="store_true", help="List all departments")
    parser.add_argument("-l", "--locations", action="store_true", help="List all locations")
    parser.add_argument("-s", "--since", type=int, help="Specify how many hours back to search (optional)")
    parser.add_argument("--use-legacy-client", action="store_true", help="Use legacy ZDX client instead of OneAPI client")

    args = parser.parse_args()

    # Set up logging
    logging_level = logging.INFO if args.verbose else logging.WARNING
    if args.quiet:
        logging_level = logging.ERROR
    logging.basicConfig(level=logging_level)

    # Initialize client based on the flag
    if args.use_legacy_client:
        # Legacy client configuration
        ZDX_CLIENT_ID = os.getenv("ZDX_CLIENT_ID")
        ZDX_CLIENT_SECRET = os.getenv("ZDX_CLIENT_SECRET")
        
        if not ZDX_CLIENT_ID or not ZDX_CLIENT_SECRET:
            print("Error: ZDX_CLIENT_ID and ZDX_CLIENT_SECRET environment variables are required for legacy client.")
            return

        config = {
            "key_id": ZDX_CLIENT_ID,
            "key_secret": ZDX_CLIENT_SECRET,
        }
        
        client = LegacyZDXClient(config)
    else:
        # OneAPI client configuration
        ZSCALER_CLIENT_ID = os.getenv("ZSCALER_CLIENT_ID")
        ZSCALER_CLIENT_SECRET = os.getenv("ZSCALER_CLIENT_SECRET")
        ZSCALER_VANITY_DOMAIN = os.getenv("ZSCALER_VANITY_DOMAIN")
        
        if not ZSCALER_CLIENT_ID or not ZSCALER_CLIENT_SECRET:
            print("Error: ZSCALER_CLIENT_ID and ZSCALER_CLIENT_SECRET environment variables are required for OneAPI client.")
            return

        config = {
            'clientId': ZSCALER_CLIENT_ID,
            'clientSecret': ZSCALER_CLIENT_SECRET,
        }
        
        # Add vanity domain if provided
        if ZSCALER_VANITY_DOMAIN:
            config['vanityDomain'] = ZSCALER_VANITY_DOMAIN
        
        client = ZscalerClient(config)

    # Handle --departments
    if args.departments:
        query_params = {}
        if args.since:
            query_params["since"] = args.since
        
        dept_list, _, err = client.zdx.admin.list_departments(query_params=query_params)
        if err:
            print(f"Error listing departments: {err}")
            return
        
        # Convert to list of dictionaries for display
        departments_data = []
        for dept in dept_list:
            if hasattr(dept, 'as_dict'):
                departments_data.append(dept.as_dict())
            else:
                departments_data.append(dept)
        
        display_table(["ID", "Name"], departments_data)

    # Handle --locations
    elif args.locations:
        query_params = {}
        if args.since:
            query_params["since"] = args.since
        
        locations_list, _, err = client.zdx.admin.list_locations(query_params=query_params)
        if err:
            print(f"Error listing locations: {err}")
            return
        
        # Convert to list of dictionaries for display
        locations_data = []
        for location in locations_list:
            if hasattr(location, 'as_dict'):
                locations_data.append(location.as_dict())
            else:
                locations_data.append(location)
        
        display_table(["ID", "Name"], locations_data)

    else:
        print("Invalid choice. Please use -d for departments or -l for locations.")


def display_table(headers, data):
    table = PrettyTable(headers)
    for item in data:
        table.add_row([item.get(header.lower()) for header in headers])
    print(table)


if __name__ == "__main__":
    main()
