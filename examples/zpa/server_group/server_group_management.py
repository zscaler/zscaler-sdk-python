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
server_group_management.py
==========================

Manage Server Groups for Zscaler Private Access (ZPA).

**Usage**::

    python3 server_group_management.py [options]

Options:
    -l, --list                    List all server groups.
    -g, --get <GROUP_ID>          Get details of a server group by ID.
    -n, --get_by_name <NAME>      Get details of a server group by name.
    -a, --add                     Add a new server group. Can provide details via command-line or prompts.
    -u, --update <GROUP_ID>       Update an existing server group. Prompts for details.
    -d, --delete <GROUP_ID>       Delete a server group by its ID.
    -h, --help                    Show this help message and exit.
"""

import argparse
import json
import os
from zscaler import ZPAClientHelper
from zscaler.utils import str2bool

# Initialize ZIAClientHelper with environment variables
ZPA_CLIENT_ID = os.getenv("ZPA_CLIENT_ID")
ZPA_CLIENT_SECRET = os.getenv("ZPA_CLIENT_SECRET")
ZPA_CUSTOMER_ID = os.getenv("ZPA_CUSTOMER_ID")
ZPA_CLOUD = os.getenv("ZPA_CLOUD")


def main():
    parser = argparse.ArgumentParser(description="Manage Server Groups for ZPA.")
    parser.add_argument("-l", "--list", action="store_true", help="List all server groups.")
    parser.add_argument("-g", "--get", metavar="GROUP_ID", help="Get details of a server group by ID.")
    parser.add_argument(
        "-n",
        "--get_by_name",
        metavar="NAME",
        help="Get details of a server group by name.",
    )
    parser.add_argument("-a", "--add", action="store_true", help="Add a new server group.")
    parser.add_argument("-u", "--update", metavar="GROUP_ID", help="Update an existing server group.")
    parser.add_argument("-d", "--delete", metavar="GROUP_ID", help="Delete a server group by its ID.")
    parser.add_argument("--name", help="Name of the server group")
    parser.add_argument("--description", help="Description of the server group")
    parser.add_argument(
        "--dynamic_discovery",
        type=str2bool,
        help="Whether dynamic discovery is enabled",
    )
    parser.add_argument("--enabled", type=str2bool, help="Whether the server group is enabled")
    parser.add_argument("--app_connector_group_ids", help="App Connector Group IDs (comma-separated)")
    parser.add_argument(
        "--server_ids",
        help="Server IDs (comma-separated, required if dynamic discovery is false)",
    )
    args = parser.parse_args()

    client = ZPAClientHelper(
        client_id=ZPA_CLIENT_ID,
        client_secret=ZPA_CLIENT_SECRET,
        customer_id=ZPA_CUSTOMER_ID,
        cloud=ZPA_CLOUD,
    )

    if args.list:
        list_server_groups(client)
    elif args.get:
        get_server_group(client, args.get)
    elif args.get_by_name:
        get_server_group_by_name(client, args.get_by_name)
    elif args.add:
        add_server_group(client, args)
    elif args.update:
        update_server_group(client, args.update, args)
    elif args.delete:
        delete_server_group(client, args.delete)
    else:
        parser.print_help()


def list_server_groups(client):
    groups = client.server_groups.list_groups()
    print(json.dumps(groups, indent=4))


def get_server_group(client, group_id):
    group = client.server_groups.get_group(group_id)
    print(json.dumps(group, indent=4))


def get_server_group_by_name(client, name):
    group = client.server_groups.get_server_group_by_name(name)
    print(json.dumps(group, indent=4))


def add_server_group(client, args):
    name = args.name if args.name else input("Enter the name of the server group: ")
    description = args.description if args.description else input("Enter the description of the server group: ")
    if args.dynamic_discovery is not None:
        dynamic_discovery = str2bool(args.dynamic_discovery)
    else:
        dynamic_discovery_input = input("Is dynamic discovery enabled? (True/False): ")
        dynamic_discovery = str2bool(dynamic_discovery_input)
    enabled = (
        args.enabled if args.enabled is not None else input("Is the server group enabled? (True/False): ").lower() == "true"
    )
    app_connector_group_ids = (
        args.app_connector_group_ids.split(",")
        if args.app_connector_group_ids
        else input("Enter App Connector Group IDs (comma-separated): ").split(",")
    )
    server_ids = (
        args.server_ids.split(",")
        if args.server_ids
        else (
            None
            if dynamic_discovery
            else input("Enter Server IDs (comma-separated, required if dynamic discovery is false): ").split(",")
        )
    )

    kwargs = {
        "name": name,
        "description": description,
        "dynamic_discovery": dynamic_discovery,
        "enabled": enabled,
        "app_connector_group_ids": app_connector_group_ids,
    }
    if server_ids:
        kwargs["server_ids"] = server_ids

    group = client.server_groups.add_group(**kwargs)
    print("Server Group added successfully:", json.dumps(group, indent=4))


def update_server_group(client, group_id, args):
    current_group = client.server_groups.get_group(group_id)
    print("Updating server group:", json.dumps(current_group, indent=4))
    # Example implementation, you need to add the logic for updating server group based on args


def delete_server_group(client, group_id):
    client.server_groups.delete_group(group_id)
    print(f"Server Group {group_id} deleted successfully.")


if __name__ == "__main__":
    main()
