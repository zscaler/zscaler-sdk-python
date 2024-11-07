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
vpn_credential_bulk_delete.py
=============================

Bulk delete VPN credentials for Zscaler Internet Access (ZIA). This script allows the deletion of multiple VPN credentials in a single operation, up to a maximum of 100 credentials per request. It utilizes environment variables for authentication with the Zscaler Internet Access (ZIA) platform. The script can also list all VPN credentials currently configured.

Usage:
    python3 vpn_credential_bulk_delete.py [-h] [-v] [-q] [-bd CREDENTIAL_IDS [CREDENTIAL_IDS ...]] [-l]

Options:
    -h, --help          Show this help message and exit.
    -v, --verbose       Increase verbosity of output. Can be used multiple times.
    -q, --quiet         Suppress output.
    -bd, --bulk-delete  Provide one or more credential IDs separated by spaces for bulk deletion.
    -l, --list          List all VPN credentials.

Examples:
    Bulk delete VPN credentials by providing their IDs:
        $ python3 vpn_credential_bulk_delete.py --bulk-delete 12345 67890 24680

    List all VPN credentials:
        $ python3 vpn_credential_bulk_delete.py --list

Environment Variables:
    ZIA_USERNAME: Username for ZIA.
    ZIA_PASSWORD: Password for ZIA.
    ZIA_API_KEY:  API key for ZIA.
    ZIA_CLOUD:    ZIA cloud name.

Please ensure that the ZIA environment variables are set before running this script.
"""

from zscaler import ZIAClientHelper
import os
import argparse
import time


def main():
    parser = argparse.ArgumentParser(description="Manage VPN credentials for a cloud service provider.")
    parser.add_argument(
        "-bd",
        "--bulk-delete",
        nargs="+",
        help="Bulk delete VPN credentials. Provide one or more credential IDs separated by spaces.",
    )
    parser.add_argument("-l", "--list", action="store_true", help="List all VPN credentials.")

    args = parser.parse_args()

    # Initialize SDK
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

    if args.bulk_delete:
        zia.traffic.bulk_delete_vpn_credentials(credential_ids=args.bulk_delete)
        print("VPN credentials successfully deleted.")
        changes_made = True

    elif args.list:
        credentials = zia.traffic.list_vpn_credentials()
        for credential in credentials:
            print(credential)

    # Activate changes if bulk deletion was performed
    if changes_made:
        print("Activating configuration changes. Please wait...")
        time.sleep(5)  # Delay for 5 seconds before activating
        activation_status = zia.activate.activate()
        print("Configuration changes activated successfully. Status:", activation_status)


if __name__ == "__main__":
    main()
