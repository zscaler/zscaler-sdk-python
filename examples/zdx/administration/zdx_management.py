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

    zdx_management.py [-h] [-v] [-q] [-d] [-l] [-s HOURS]

**Examples**:

List all Departments:
    $ python zdx_management.py -d

List all Locations:
    $ python zdx_management.py -l

List Departments for the past 5 hours:
    $ python zdx_management.py -d -s 5

"""

import argparse
import logging
import json
import os
from prettytable import PrettyTable
from zscaler.zdx import ZDXClientHelper
from zscaler.zdx.admin import AdminAPI


def main():
    parser = argparse.ArgumentParser(description="Manage Departments and Locations for Zscaler Digital Experience (ZDX)")
    parser.add_argument("-v", "--verbose", action="count", help="Verbose (-vv for extra verbose)")
    parser.add_argument("-q", "--quiet", action="store_true", help="Suppress all output")
    parser.add_argument("-d", "--departments", action="store_true", help="List all departments")
    parser.add_argument("-l", "--locations", action="store_true", help="List all locations")
    parser.add_argument("-s", "--since", type=int, help="Specify how many hours back to search (optional)")

    args = parser.parse_args()

    # Set up logging
    logging_level = logging.INFO if args.verbose else logging.WARNING
    if args.quiet:
        logging_level = logging.ERROR
    logging.basicConfig(level=logging_level)

    # Initialize ZDXClientHelper
    ZDX_CLIENT_ID = os.getenv("ZDX_CLIENT_ID")
    ZDX_CLIENT_SECRET = os.getenv("ZDX_CLIENT_SECRET")

    client = ZDXClientHelper(
        client_id=ZDX_CLIENT_ID,
        client_secret=ZDX_CLIENT_SECRET,
    )

    admin_api = AdminAPI(client)

    # Handle --departments
    if args.departments:
        since = args.since if args.since else None
        departments = admin_api.list_departments(since=since)
        display_table(["ID", "Name"], departments)

    # Handle --locations
    elif args.locations:
        since = args.since if args.since else None
        locations = admin_api.list_locations(since=since)
        display_table(["ID", "Name"], locations)

    else:
        print("Invalid choice. Please use -d for departments or -l for locations.")


def display_table(headers, data):
    table = PrettyTable(headers)
    for item in data:
        table.add_row([item.get(header.lower()) for header in headers])
    print(table)


if __name__ == "__main__":
    main()
