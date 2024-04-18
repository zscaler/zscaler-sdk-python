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
machine_group_management.py
===========================

Retrieves Machine Group for Zscaler Private Access (ZPA).

**Usage**::

    machine_group_management.py [-h] [-v] [-q] [-l] [-g PROFILE_ID] [-n PROFILE_NAME] [additional_args]

**Examples**:

List all Machine Group :
    $ python3 machine_group_management.py -l

Get details of a specific Machine Group by ID:
    $ python3 machine_group_management.py -g 99999

Get details of a specific Machine Group by Name:
    $ python3 machine_group_management.py -n "Group_Name"
"""


import argparse
import json
import os
from zscaler import ZPAClientHelper


def main():
    parser = argparse.ArgumentParser(description="Manage Machine Group for ZPA.")
    parser.add_argument("-l", "--list", action="store_true", help="List all machine groups.")
    parser.add_argument("-g", "--get", metavar="GROUP_ID", help="Get details of an machine group by ID.")
    parser.add_argument(
        "-n",
        "--get_by_name",
        metavar="NAME",
        help="Get details of machine group by name.",
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
        list_groups(client)
    elif args.get:
        get_group(client, args.get)
    elif args.get_by_name:
        get_machine_group_by_name(client, args.get_by_name)


def list_groups(client):
    groups = client.machine_groups.list_groups()
    print(json.dumps(groups, indent=4))


def get_group(client, group_id):
    group = client.machine_groups.get_group(group_id)
    if group:
        print(json.dumps(group, indent=4))
    else:
        print(f"No machine group found with ID {group_id}")


def get_machine_group_by_name(client, name):
    group = client.machine_groups.get_machine_group_by_name(name)
    if group:
        print(json.dumps(group, indent=4))
    else:
        print(f"No machine group found with name {name}")


if __name__ == "__main__":
    main()
