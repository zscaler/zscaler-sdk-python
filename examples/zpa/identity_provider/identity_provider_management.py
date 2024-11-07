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
identity_provider_management.py
===========================

Retrieves Identity Provider for Zscaler Private Access (ZPA).

**Usage**::

    identity_provider_management.py [-h] [-v] [-q] [-l] [-g PROFILE_ID] [-n PROFILE_NAME] [additional_args]

**Examples**:

List all Identity Providers :
    $ python3 identity_provider_management.py -l

Get details of a specific Identity Provider by ID:
    $ python3 identity_provider_management.py -g 99999

Get details of a specific Identity Provider by Name:
    $ python3 identity_provider_management.py -n "IdP_Name"
"""


import argparse
import json
import os
from zscaler import ZPAClientHelper


def main():
    parser = argparse.ArgumentParser(description="Manage Identity Provider for ZPA.")
    parser.add_argument("-l", "--list", action="store_true", help="List all Identity Providers.")
    parser.add_argument(
        "-g",
        "--get",
        metavar="IDP_ID",
        help="Get details of an Identity Provider by ID.",
    )
    parser.add_argument(
        "-n",
        "--get_by_name",
        metavar="NAME",
        help="Get details of Identity Provider by name.",
    )
    args = parser.parse_args()

    # Initialize ZIAClientHelper
    client = ZPAClientHelper(
        client_id=os.getenv("ZPA_CLIENT_ID"),
        client_secret=os.getenv("ZPA_CLIENT_SECRET"),
        customer_id=os.getenv("ZPA_CUSTOMER_ID"),
        cloud=os.getenv("ZPA_CLOUD"),
    )

    if args.list:
        list_idps(client)
    elif args.get:
        get_idp(client, args.get)
    elif args.get_by_name:
        get_idp_by_name(client, args.get_by_name)


def list_idps(client):
    idps = client.idp.list_idps()
    print(json.dumps(idps, indent=4))


def get_idp(client, idp_id):
    idp = client.idp.get_idp(idp_id)
    if idp:
        print(json.dumps(idp, indent=4))
    else:
        print(f"No identity provider found with ID {idp_id}")


def get_idp_by_name(client, name):
    idp = client.idp.get_idp_by_name(name)
    if idp:
        print(json.dumps(idp, indent=4))
    else:
        print(f"No identity provider found with name {name}")


if __name__ == "__main__":
    main()
