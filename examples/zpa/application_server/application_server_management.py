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
application_server_management.py
===========================

Manage Application Server for Zscaler Private Access (ZPA).

**Usage**::

    application_server_management.py [-h] [-v] [-q] [-l] [-g SERVER_ID] [-n SERVER_NAME] [-d SERVER_ID] [--add] [--update SERVER_ID] [additional_args]

**Examples**:

List all Application Servers:
    $ python3 application_server_management.py -l

Get details of a specific Application Server by ID:
    $ python3 application_server_management.py -g 99999

Get details of a specific Application Server by Name:
    $ python3 application_server_management.py -n "Server Name"

Add a new Application Server:
    $ python3 application_server_management.py --add --name "New Application Server" --enabled True --description "Application Server Description" --address "192.168.100.10"

Update an existing Application Server:
    $ python3 application_server_management.py --update 99999 --name "Updated Application Server Name"

Delete a Application Server by ID:
    $ python3 application_server_management.py -d 99999

"""

import argparse
import logging
import os
import json
from zscaler import ZPAClientHelper
from zscaler.utils import str2bool


# Initialize ZIAClientHelper with environment variables
ZPA_CLIENT_ID = os.getenv("ZPA_CLIENT_ID")
ZPA_CLIENT_SECRET = os.getenv("ZPA_CLIENT_SECRET")
ZPA_CUSTOMER_ID = os.getenv("ZPA_CUSTOMER_ID")
ZPA_CLOUD = os.getenv("ZPA_CLOUD")


def main():
    parser = argparse.ArgumentParser(description="Manage Application Server for Zscaler Private Access (ZPA)")
    parser.add_argument("-v", "--verbose", action="count", help="Verbose (-vv for extra verbose)")
    parser.add_argument("-q", "--quiet", action="store_true", help="Suppress all output")
    parser.add_argument("-l", "--list", action="store_true", help="List all application servers")
    parser.add_argument(
        "-g",
        "--get",
        metavar="SERVER_ID",
        help="Get details of an application server by ID",
    )
    parser.add_argument(
        "-n",
        "--get_by_name",
        metavar="SERVER_NAME",
        help="Get details of an application server by name",
    )
    parser.add_argument("-d", "--delete", metavar="SERVER_ID", help="Delete an application server by ID")
    parser.add_argument("--add", action="store_true", help="Add a new application server")
    parser.add_argument("--update", metavar="SERVER_ID", help="Update an existing application server")
    parser.add_argument("--name", help="Name of the application server")
    parser.add_argument("--description", help="Description of the application server")
    parser.add_argument("--enabled", type=str2bool, help="Whether the application server is enabled")
    parser.add_argument("--address", help="The domain or IP address of the server.")

    args = parser.parse_args()

    # Set up logging
    logging_level = logging.INFO if args.verbose else logging.WARNING
    if args.quiet:
        logging_level = logging.ERROR
    logging.basicConfig(level=logging_level)

    client = ZPAClientHelper(
        client_id=ZPA_CLIENT_ID,
        client_secret=ZPA_CLIENT_SECRET,
        customer_id=ZPA_CUSTOMER_ID,
        cloud=ZPA_CLOUD,
    )

    if args.list:
        servers = client.servers.list_servers()
        if servers:
            print(json.dumps(servers, indent=4))
        else:
            print("No application servers available.")

    elif args.get:
        server = client.servers.get_server(args.get)
        if server:
            print(json.dumps(server, indent=4))
        else:
            print(f"No application server found with ID {args.get}.")

    elif args.get_by_name:
        server = client.servers.get_server_by_name(args.get_by_name)
        if server:
            print(json.dumps(server, indent=4))
        else:
            print(f"No application server found with name '{args.get_by_name}'.")

    elif args.delete:
        response_code = client.servers.delete_server(args.delete)
        if response_code == 204:
            print(f"Application server {args.delete} deleted successfully.")
        else:
            print(f"Failed to delete application server {args.delete}. Response code: {response_code}")

    elif args.add:
        new_server = client.servers.add_server(
            name=args.name,
            description=args.description,
            enabled=args.enabled,
            address=args.address,
        )
        print("Application server added successfully:", json.dumps(new_server, indent=4))

    elif args.update:
        updated_server = client.servers.update_server(
            server_id=args.update,
            name=args.name,
            description=args.description,
            enabled=args.enabled,
            address=args.address,
        )
        print(
            f"Application server {args.update} updated successfully:",
            json.dumps(updated_server, indent=4),
        )


if __name__ == "__main__":
    main()
