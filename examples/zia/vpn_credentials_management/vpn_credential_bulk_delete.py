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

# Author:

from zscaler import ZIAClientHelper
import os
import argparse
import logging

"""
vpn_credential_bulk_delete.py
=============================

Bulk delete VPN credentials for Zscaler Internet Access (ZIA). This script allows the deletion of multiple VPN credentials in a single operation, up to a maximum of 100 credentials per request. It utilizes environment variables for authentication with the Zscaler Internet Access (ZIA) platform. The script can also list all VPN credentials currently configured.

Usage:
    python vpn_credential_bulk_delete.py [-h] [-v] [-q] [-bd CREDENTIAL_IDS [CREDENTIAL_IDS ...]] [-l]

Options:
    -h, --help          Show this help message and exit.
    -v, --verbose       Increase verbosity of output. Can be used multiple times.
    -q, --quiet         Suppress output.
    -bd, --bulk-delete  Provide one or more credential IDs separated by spaces for bulk deletion.
    -l, --list          List all VPN credentials.

Examples:
    Bulk delete VPN credentials by providing their IDs:
        $ python vpn_credential_bulk_delete.py --bulk-delete 12345 67890 24680

    List all VPN credentials:
        $ python vpn_credential_bulk_delete.py --list

Environment Variables:
    ZIA_USERNAME: Username for ZIA.
    ZIA_PASSWORD: Password for ZIA.
    ZIA_API_KEY:  API key for ZIA.
    ZIA_CLOUD:    ZIA cloud name.

Please ensure that the ZIA environment variables are set before running this script.
"""

def main():
    parser = argparse.ArgumentParser(
        description="Manage VPN credentials for a cloud service provider."
    )
    parser.add_argument(
        "-v", "--verbose", action="count", help="Verbose (-vv for extra verbose)."
    )
    parser.add_argument("-q", "--quiet", action="store_true", help="No output.")
    parser.add_argument(
        "-bd", "--bulk-delete", nargs='+', help="Bulk delete VPN credentials. Provide one or more credential IDs separated by spaces."
    )
    parser.add_argument(
        "-l", "--list", action="store_true", help="List all VPN credentials."
    )
    
    args = parser.parse_args()

    # Set up logging
    if args.verbose is None:
        args.verbose = 0
    if not args.quiet:
        logging_level = 20 - (args.verbose * 10)
        logging.basicConfig(level=logging_level)

    # Initialize SDK
    ZIA_USERNAME = os.getenv("ZIA_USERNAME")
    ZIA_PASSWORD = os.getenv("ZIA_PASSWORD")
    ZIA_API_KEY = os.getenv("ZIA_API_KEY")
    ZIA_CLOUD = os.getenv("ZIA_CLOUD")
    zia = ZIAClientHelper(username=ZIA_USERNAME, password=ZIA_PASSWORD, api_key=ZIA_API_KEY, cloud=ZIA_CLOUD)

    if args.bulk_delete:
        response_code = zia.traffic.bulk_delete_vpn_credentials(credential_ids=args.bulk_delete)
        if response_code == 204:
            print("VPN credentials successfully deleted.")
        else:
            print(f"Failed to delete VPN credentials. Response code: {response_code}")

    elif args.list:
        credentials = zia.traffic.list_vpn_credentials()
        for credential in credentials:
            print(credential)

if __name__ == "__main__":
    main()
