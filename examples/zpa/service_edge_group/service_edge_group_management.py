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
service_edge_group_management.py
=============================

Manage Service Edge Groups for Zscaler Private Access (ZPA).

**Usage**::

    service_edge_group_management.py [-h] [-v] [-q] [-l] [-g GROUP_ID] [-n GROUP_NAME] [-d GROUP_ID] [--add] [--update GROUP_ID] [additional_args]

**Examples**:

List all Service Edge Group s:
    $ python3 service_edge_group_management.py -l

Get details of a specific Service Edge Group  by ID:
    $ python3 service_edge_group_management.py -g 99999

Get details of a specific Service Edge Group  by Name:
    $ python3 service_edge_group_management.py -n "Service Edge Group  Name"

Add a new Service Edge Group :
    $ python3 service_edge_group_management.py --add --name "New Service Edge Group " --location "Location" --latitude 123 --longitude 456

Update an existing Service Edge Group :
    $ python3 service_edge_group_management.py --update 99999 --name "Updated Service Edge Group "

Delete a Service Edge Group by ID:
    $ python3 service_edge_group_management.py -d 99999

"""

import argparse
import logging
from zscaler import ZPAClientHelper
import json
import os
from zscaler.utils import str2bool


def main():
    parser = argparse.ArgumentParser(description="Manage App Service Edge Group s for Zscaler Private Access (ZPA)")
    parser.add_argument("-v", "--verbose", action="count", help="Verbose (-vv for extra verbose)")
    parser.add_argument("-q", "--quiet", action="store_true", help="Suppress all output")
    parser.add_argument("-l", "--list", action="store_true", help="List all Service Edge Group s")
    parser.add_argument(
        "-g",
        "--get",
        metavar="GROUP_ID",
        help="Get details of a Service Edge Group  by ID",
    )
    parser.add_argument(
        "-n",
        "--get_by_name",
        metavar="GROUP_NAME",
        help="Get details of a Service Edge Group  by name",
    )
    parser.add_argument("-d", "--delete", metavar="GROUP_ID", help="Delete a Service Edge Group  by ID")
    parser.add_argument("--add", action="store_true", help="Add a new Service Edge Group ")
    parser.add_argument("--update", metavar="GROUP_ID", help="Update an existing Service Edge Group ")
    parser.add_argument("--name", help="Name of the Service Edge Group ")
    parser.add_argument("--description", help="The description of the Service Edge Group.")
    parser.add_argument("--enabled", type=str2bool, help="Whether the Service Edge Group is enabled")
    parser.add_argument("--city_country", help="The city and country of the App Connector.")
    parser.add_argument("--country_code", help="The country code of the App Connector.")
    parser.add_argument("--latitude", type=float, help="Latitude of the Service Edge Group 's location")
    parser.add_argument(
        "--longitude",
        type=float,
        help="Longitude of the Service Edge Group 's location",
    )
    parser.add_argument("--location", help="Location name of the Service Edge Group ")
    # Define other arguments for adding/updating Service Edge Group s as needed

    args = parser.parse_args()

    # Set up logging
    logging_level = logging.INFO if args.verbose else logging.WARNING
    if args.quiet:
        logging_level = logging.ERROR
    logging.basicConfig(level=logging_level)

    # Initialize ZIAClientHelper
    ZPA_CLIENT_ID = os.getenv("ZPA_CLIENT_ID")
    ZPA_CLIENT_SECRET = os.getenv("ZPA_CLIENT_SECRET")
    ZPA_CUSTOMER_ID = os.getenv("ZPA_CUSTOMER_ID")
    ZPA_CLOUD = os.getenv("ZPA_CLOUD")

    # Initialize ZPAClient
    client = ZPAClientHelper(
        client_id=ZPA_CLIENT_ID,
        client_secret=ZPA_CLIENT_SECRET,
        customer_id=ZPA_CUSTOMER_ID,
        cloud=ZPA_CLOUD,
    )

    if args.list:
        connector_groups = client.service_edges.list_service_edge_groups()
        print(json.dumps(connector_groups, indent=4))

    elif args.get:
        connector_group = client.service_edges.get_service_edge_group(args.get)
        print(json.dumps(connector_group, indent=4) if connector_group else f"No Service Edge Group  found with ID {args.get}")

    elif args.get_by_name:
        connector_group = client.service_edges.get_service_edge_group_by_name(args.get_by_name)
        print(
            json.dumps(connector_group, indent=4)
            if connector_group
            else f"No Service Edge Group  found with name {args.get_by_name}"
        )

    elif args.delete:
        response_code = client.service_edges.delete_service_edge_group(args.delete)
        print(
            f"Service Edge Group  {args.delete} deleted successfully."
            if response_code == 204
            else f"Failed to delete Service Edge Group  {args.delete}. Response code: {response_code}"
        )

    elif args.add:
        new_group = client.service_edges.add_service_edge_group(
            name=args.name,
            latitude=args.latitude,
            longitude=args.longitude,
            location=args.location,
        )
        print(f"Service Edge Group  added successfully: {json.dumps(new_group, indent=4)}")

    elif args.update:
        updated_group = client.service_edges.update_service_edge_group(
            group_id=args.update,
            name=args.name,
            latitude=args.latitude,
            longitude=args.longitude,
            location=args.location,
        )
        print(f"Service Edge Group  {args.update} updated successfully: {json.dumps(updated_group, indent=4)}")


if __name__ == "__main__":
    main()
