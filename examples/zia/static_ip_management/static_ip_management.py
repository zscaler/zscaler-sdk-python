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
static_ip_management.py
=======================

Manage Static IPs for Zscaler Internet Access (ZIA). This script provides functionality to add, update, check, delete, and list static IP addresses within your ZIA environment. It is designed to interact with the ZIA API, simplifying the management of static IP addresses through a command-line interface.

Usage:
    static_ip_management.py [-h] [-v] [-q] [-a] [-u STATIC_IP_ID] [-d STATIC_IP_ID] [-l] [-c IP_ADDRESS] [--ip_address IP_ADDRESS] [--comment COMMENT]

Options:
    -h, --help                  Show this help message and exit.
    -v, --verbose               Increase output verbosity (use -vv for even more verbosity).
    -q, --quiet                 Suppress all output.
    -a, --add                   Add a new static IP. Requires --ip_address.
    -u, --update STATIC_IP_ID   Update an existing static IP by its ID. Requires additional arguments like --comment.
    -d, --delete STATIC_IP_ID   Delete a static IP by its ID.
    -l, --list                  List all static IPs.
    -c, --check IP_ADDRESS      Check if a static IP is valid. Requires --ip_address.
    --ip_address IP_ADDRESS     The IP address for adding, checking, or updating a static IP.
    --comment COMMENT           A comment or description for the static IP.

Examples:

Add a new static IP address:
    $ python3 static_ip_management.py -a --ip_address "192.0.2.1" --comment "New York Office"

Update a static IP (static_ip_id = '12345') with a new comment:
    $ python3 static_ip_management.py -u 12345 --comment "Updated comment for NY Office"

Delete a static IP (static_ip_id = '12345'):
    $ python3 static_ip_management.py -d 12345

List all static IPs:
    $ python3 static_ip_management.py -l

Check if a static IP address is valid:
    $ python3 static_ip_management.py -c --ip_address "185.211.32.65"

Please note that this script requires environment variables to be set for ZIA_USERNAME, ZIA_PASSWORD, ZIA_API_KEY, and ZIA_CLOUD to authenticate with the ZIA API.
"""

import argparse
import os
import json
import time
from zscaler import ZIAClientHelper


def main():
    parser = argparse.ArgumentParser(description="Manage Static IPs for Zscaler Internet Access (ZIA).")
    parser.add_argument(
        "-a",
        "--add",
        action="store_true",
        help="Add a new static IP. Requires --ip_address.",
    )
    parser.add_argument(
        "-u",
        "--update",
        metavar="STATIC_IP_ID",
        help="Update an existing static IP by its ID. Requires --ip_address and/or --comment.",
    )
    parser.add_argument("-d", "--delete", metavar="STATIC_IP_ID", help="Delete a static IP by its ID.")
    parser.add_argument("-l", "--list", action="store_true", help="List all static IPs.")
    parser.add_argument(
        "-c",
        "--check",
        metavar="IP_ADDRESS",
        help="Check if a static IP is valid. Requires --ip_address.",
    )
    parser.add_argument(
        "--ip_address",
        help="The IP address for adding, checking, or updating a static IP.",
    )
    parser.add_argument("--comment", help="A comment or description for the static IP.")

    args = parser.parse_args()

    # Initialize ZIAClientHelper
    ZIA_USERNAME = os.getenv("ZIA_USERNAME")
    ZIA_PASSWORD = os.getenv("ZIA_PASSWORD")
    ZIA_API_KEY = os.getenv("ZIA_API_KEY")
    ZIA_CLOUD = os.getenv("ZIA_CLOUD")

    zia = ZIAClientHelper(
        username=ZIA_USERNAME,
        password=ZIA_PASSWORD,
        api_key=ZIA_API_KEY,
        cloud=ZIA_CLOUD,
    )

    changes_made = False

    if args.add:
        if not args.ip_address:
            print("Error: Adding a static IP requires an --ip_address argument.")
            return
        response = zia.traffic.add_static_ip(ip_address=args.ip_address, comment=args.comment)
        print("Static IP added successfully:", json.dumps(response, indent=4))
        changes_made = True

    elif args.update:
        response = zia.traffic.update_static_ip(static_ip_id=args.update, ip_address=args.ip_address, comment=args.comment)
        print(f"Static IP {args.update} updated successfully.")
        changes_made = True

    elif args.delete:
        zia.traffic.delete_static_ip(static_ip_id=args.delete)
        print(f"Static IP {args.delete} deleted successfully.")
        changes_made = True

    elif args.list:
        static_ips = zia.traffic.list_static_ips()
        print(json.dumps(static_ips, indent=4))

    elif args.check:
        is_valid = zia.traffic.check_static_ip(ip_address=args.check)
        if is_valid:
            print(f"Static IP {args.check} is valid.")
        else:
            print(f"Static IP {args.check} is not valid or an error occurred.")

    # Activate changes if any modifications were made.
    if changes_made:
        print("Activating configuration changes. Please wait...")
        time.sleep(5)  # Delay for 5 seconds before activating.
        activation_status = zia.activate.activate()
        print("Configuration changes activated successfully. Status:", activation_status)


if __name__ == "__main__":
    main()
