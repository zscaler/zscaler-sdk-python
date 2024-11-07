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
vpn_credentials_management.py
=============================

This script is designed to manage VPN credentials within the Zscaler Internet Access (ZIA) environment. It supports adding, updating, deleting, and listing VPN credentials via command-line interface.

Usage:
    python vpn_credentials_management.py [-a {IP,UFQDN}] [--pre_shared_key KEY]
                                         [--ip_address ADDRESS] [--email EMAIL]
                                         [--comments COMMENT] [-u ID] [-d ID] [-l]

Options:
    -a, --add {IP,UFQDN}             Add a new VPN credential. Choose 'IP' or 'UFQDN' for the type.
    --pre_shared_key KEY             The pre-shared key for the VPN credential.
    --ip_address ADDRESS             The IP address, required if type is 'IP'.
    --email EMAIL                    The email address, required if type is 'UFQDN'.
    --comments COMMENT               Optional comments for the VPN credential.
    -u, --update ID                  Update an existing VPN credential by ID.
    -d, --delete ID                  Delete an existing VPN credential by ID.
    -l, --list                       List all VPN credentials.

Examples:
    Add a new IP-based VPN credential:
        python3 vpn_credentials_management.py -a IP --pre_shared_key mykey123 --ip_address 203.0.113.50 --comments "HQ VPN"

    Add a new UFQDN-based VPN credential:
        python3 vpn_credentials_management.py -a UFQDN --pre_shared_key '<YourPreSharedKey>' --email test1@example.com --comments "HQ VPN"

    Update a VPN credential (ID: 12345) with a new comment:
        python3 vpn_credentials_management.py -u 12345 --comments "Updated HQ VPN"

    Delete a VPN credential (ID: 12345):
        python3 vpn_credentials_management.py -d 12345

    List all VPN credentials:
        python3 vpn_credentials_management.py -l
"""

import argparse
import os
import json
import time
from zscaler import ZIAClientHelper


def main():
    parser = argparse.ArgumentParser(description="Manage VPN credentials for a cloud service provider.")
    parser.add_argument(
        "-a",
        "--add",
        choices=["IP", "UFQDN"],
        help="Add a new VPN credential of type IP or UFQDN.",
    )
    parser.add_argument("-u", "--update", help="Credential ID to update an existing VPN credential.")
    parser.add_argument("-d", "--delete", help="Credential ID to delete an existing VPN credential.")
    parser.add_argument("-l", "--list", action="store_true", help="List all VPN credentials.")

    # VPN credential arguments for add and update
    parser.add_argument("--pre_shared_key", help="Pre-shared key for the VPN credential.")
    parser.add_argument(
        "--ip_address",
        help="IP address for the VPN credential (required for IP auth type).",
    )
    parser.add_argument(
        "--email",
        help="Email address for the VPN credential (required for UFQDN auth type).",
    )
    parser.add_argument("--comments", help="Comments for the VPN credential.")
    parser.add_argument("--credential_id", help="Location ID associated with the VPN credential.")

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
        response = None
        if args.add == "IP" and args.ip_address:
            response = zia.traffic.add_vpn_credential(
                authentication_type=args.add,
                pre_shared_key=args.pre_shared_key,
                ip_address=args.ip_address,
                comments=args.comments,
            )
            print(
                "IP-based VPN credential added successfully:",
                json.dumps(response, indent=4),
            )
            changes_made = True
        elif args.add == "UFQDN" and args.email:
            response = zia.traffic.add_vpn_credential(
                authentication_type=args.add,
                pre_shared_key=args.pre_shared_key,
                fqdn=args.email,
                comments=args.comments,
            )
            print(
                "UFQDN-based VPN credential added successfully:",
                json.dumps(response, indent=4),
            )
            changes_made = True
        else:
            print("Error: Missing required fields for the selected authentication type.")

    elif args.update:
        zia.traffic.update_vpn_credential(
            credential_id=args.update,
            pre_shared_key=args.pre_shared_key,
            comments=args.comments,
        )
        print("VPN credential updated successfully.")
        changes_made = True

    elif args.delete:
        zia.traffic.delete_vpn_credential(credential_id=args.delete)
        print("VPN credential deleted successfully.")
        changes_made = True

    elif args.list:
        credentials = zia.traffic.list_vpn_credentials()
        print(json.dumps(credentials, indent=4))

    if changes_made:
        print("Activating configuration changes. Please wait...")
        time.sleep(5)  # Delay for 5 seconds before activating.
        activation_status = zia.activate.activate()
        print("Configuration changes activated successfully. Status:", activation_status)


if __name__ == "__main__":
    main()
