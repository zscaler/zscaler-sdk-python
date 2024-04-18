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
scim_groups_management.py
=========================

Manages SCIM Groups for Zscaler Private Access (ZPA).

**Usage**:
    python3 scim_groups_management.py [-h] [-l IDP_NAME] [-g GROUP_ID] [--search_name GROUP_NAME]

**Options**:
    -h, --help              Show this help message and exit.
    -l IDP_NAME             List all SCIM Groups for a given IdP name.
    -g GROUP_ID             Get details of a SCIM Group by its ID.
    --search_name GROUP_NAME Search a SCIM Group by its name.

**Examples**:
    Listing all SCIM Groups by IDP Name:
        $ python3 scim_groups_management.py -l "IDP_NAME"

    Getting details of a SCIM Group by Name:
        $ python3 scim_groups_management.py --search_name "GROUP_NAME"

    Getting details of a SCIM Group by ID:
        $ python3 scim_groups_management.py -g "GROUP_ID"
"""

import argparse
import json
import os
from zscaler import ZPAClientHelper


def main():
    parser = argparse.ArgumentParser(description="Retrieves SCIM Groups from the ZPA cloud.")
    parser.add_argument(
        "-l",
        "--list",
        metavar="IDP_NAME",
        help="List all SCIM Groups for a given IdP name.",
    )
    parser.add_argument("-g", "--get", metavar="GROUP_ID", help="Get details of a SCIM Group by its ID.")
    parser.add_argument("--search_name", metavar="GROUP_NAME", help="Search a SCIM Group by its name.")
    args = parser.parse_args()

    client = ZPAClientHelper(
        client_id=os.getenv("ZPA_CLIENT_ID"),
        client_secret=os.getenv("ZPA_CLIENT_SECRET"),
        customer_id=os.getenv("ZPA_CUSTOMER_ID"),
        cloud=os.getenv("ZPA_CLOUD"),
    )

    if args.list:
        list_groups_by_idp_name(client, args.list)
    elif args.get:
        get_group(client, args.get)
    elif args.search_name:
        search_group_by_name(client, args.search_name)


def list_groups_by_idp_name(client, idp_name):
    idps = client.idp.list_idps()
    idp_id = next((idp["id"] for idp in idps if idp["name"] == idp_name), None)
    if idp_id:
        groups = client.scim_groups.list_groups(idp_id=idp_id)
        print(json.dumps(groups, indent=4))
    else:
        print(f"No IdP found with name {idp_name}")


def get_group(client, group_id):
    group = client.scim_groups.get_group(group_id)
    if group:
        print(json.dumps(group, indent=4))
    else:
        print(f"No SCIM Group found with ID {group_id}")


def search_group_by_name(client, group_name):
    # This method assumes all groups are listed and then filtered by name, which is not efficient.
    # A more efficient approach requires direct support from the API for searching by name.
    idps = client.idp.list_idps()
    for idp in idps:
        groups = client.scim_groups.list_groups(idp_id=idp["id"])
        for group in groups:
            if group["name"].lower() == group_name.lower():
                print(json.dumps(group, indent=4))
                return
    print(f"No SCIM Group found with name {group_name}")


if __name__ == "__main__":
    main()
