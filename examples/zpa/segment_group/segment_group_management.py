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
segment_group_management.py
===========================

Manage Segment Groups for Zscaler Private Access (ZPA).

**Usage**::

    segment_group_management.py [-h] [-v] [-q] [-l] [-g GROUP_ID] [-n GROUP_NAME] [-d GROUP_ID] [--add] [--update GROUP_ID] [additional_args]

**Examples**:

List all Segment Groups:
    $ python segment_group_management.py -l

Get details of a specific Segment Group by ID:
    $ python segment_group_management.py -g 99999

Get details of a specific Segment Group by Name:
    $ python segment_group_management.py -n "Group Name"

Add a new Segment Group:
    $ python segment_group_management.py --add --name "New Group" --enabled True --description "Group Description"

Update an existing Segment Group:
    $ python segment_group_management.py --update 99999 --name "Updated Group Name"

Delete a Segment Group by ID:
    $ python segment_group_management.py -d 99999

"""

import argparse
import logging
from zscaler import ZPAClientHelper
import json
import os
from zscaler.utils import str2bool


def main():
    parser = argparse.ArgumentParser(description="Manage Segment Groups for a Cloud Service Provider.")
    parser.add_argument("-v", "--verbose", action="count", help="Verbose (-vv for extra verbose)")
    parser.add_argument("-q", "--quiet", action="store_true", help="Suppress all output")
    parser.add_argument("-l", "--list", action="store_true", help="List all segment groups")
    parser.add_argument("-g", "--get", metavar="GROUP_ID", help="Get details of a segment group by ID")
    parser.add_argument(
        "-n",
        "--get_by_name",
        metavar="GROUP_NAME",
        help="Get details of a segment group by name",
    )
    parser.add_argument("-d", "--delete", metavar="GROUP_ID", help="Delete a segment group by ID")
    parser.add_argument("--add", action="store_true", help="Add a new segment group")
    parser.add_argument("--update", metavar="GROUP_ID", help="Update an existing segment group")
    parser.add_argument("--name", help="Name of the segment group")
    parser.add_argument("--enabled", type=str2bool, help="Whether the segment group is enabled")
    parser.add_argument("--description", help="Description of the segment group")
    # Define other arguments for adding/updating segment groups as needed

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
        segment_groups = client.segment_groups.list_groups()
        print(json.dumps(segment_groups, indent=4))

    elif args.get:
        segment_group = client.segment_groups.get_group(args.get)
        print(json.dumps(segment_group, indent=4) if segment_group else f"No segment group found with ID {args.get}")

    elif args.get_by_name:
        segment_group = client.segment_groups.get_segment_group_by_name(args.get_by_name)
        print(json.dumps(segment_group, indent=4) if segment_group else f"No segment group found with name {args.get_by_name}")

    elif args.delete:
        response_code = client.segment_groups.delete_group(args.delete)
        print(
            f"Segment Group {args.delete} deleted successfully."
            if response_code == 204
            else f"Failed to delete Segment Group {args.delete}. Response code: {response_code}"
        )

    elif args.add:
        new_group = client.segment_groups.add_group(name=args.name, enabled=args.enabled, description=args.description)
        print(f"Segment Group added successfully: {json.dumps(new_group, indent=4)}")

    elif args.update:
        updated_group = client.segment_groups.update_group(
            group_id=args.update,
            name=args.name,
            enabled=args.enabled,
            description=args.description,
        )
        print(f"Segment Group {args.update} updated successfully: {json.dumps(updated_group, indent=4)}")


if __name__ == "__main__":
    main()
