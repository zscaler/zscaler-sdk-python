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
import json
import argparse
import logging

"""
vpn_credentials_management.py
==========================

Manage VPN credentials for Zscaler Internet Access (ZIA).

**Usage**::

    vpn_credentials_management.py [-h] [-v] [-q] [-a] [-u] [-d] [-l] [additional_args]

**Examples**:

Add VPN credential using IP authentication type:

    $ python vpn_credentials_management.py -a IP MyPreSharedKey --ip_address 203.0.113.40 --comments "NY Branch Office"

Update VPN credential (credential_id = '12345') with new comments:

    $ python vpn_credentials_management.py -u 12345 --comments "Updated NY Office comment"

List all VPN credentials:

    $ python vpn_credentials_management.py -l

Delete VPN credential (credential_id = '12345'):

    $ python vpn_credentials_management.py -d 12345
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
        "-a", "--add", choices=['IP', 'UFQDN'], help="Add a new VPN credential of type IP or UFQDN."
    )
    parser.add_argument(
        "-u", "--update", help="Credential ID to update an existing VPN credential."
    )
    parser.add_argument(
        "-d", "--delete", help="Credential ID to delete an existing VPN credential."
    )
    parser.add_argument(
        "-l", "--list", action="store_true", help="List all VPN credentials."
    )
    
    # VPN credential arguments for add and update
    parser.add_argument("--pre_shared_key", help="Pre-shared key for the VPN credential.")
    parser.add_argument("--ip_address", help="IP address for the VPN credential (required for IP auth type).")
    parser.add_argument("--email", help="Email address for the VPN credential (required for UFQDN auth type).")
    parser.add_argument("--comments", help="Comments for the VPN credential.")
    parser.add_argument("--credential_id", help="Location ID associated with the VPN credential.")

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

    if args.add:
        response = None  # Initialize response variable
        if args.add == "IP" and args.ip_address:
            response = zia.traffic.add_vpn_credential(authentication_type=args.add,
                                                    pre_shared_key=args.pre_shared_key,
                                                    ip_address=args.ip_address,
                                                    comments=args.comments)
            print("IP-based VPN credential added successfully.")
        elif args.add == "UFQDN" and args.email:
            response = zia.traffic.add_vpn_credential(authentication_type=args.add,
                                                    pre_shared_key=args.pre_shared_key,
                                                    fqdn=args.email,
                                                    comments=args.comments)
            print("UFQDN-based VPN credential added successfully.")
        
        if response:
            # Assuming 'response' is a dictionary-like object that can be directly serialized
            print("API Response:", json.dumps(response, indent=4))
        else:
            if not args.ip_address or not args.email:
                print("Error: IP address is required for IP type, and email is required for UFQDN type.")

    elif args.update:
        zia.traffic.update_vpn_credential(credential_id=args.update,
                                  pre_shared_key=args.pre_shared_key,
                                  comments=args.comments,)
        print("VPN credential updated successfully.")

    elif args.delete:
        zia.traffic.delete_vpn_credential(credential_id=args.delete)
        print("VPN credential deleted successfully.")

    elif args.list:
        credentials = zia.traffic.list_vpn_credentials()
        for credential in credentials:
            print(credential)

if __name__ == "__main__":
    main()