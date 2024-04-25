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
application_segment_management.py
=================================

Manage Application Segments for Zscaler Private Access (ZPA).

**Usage**::

    application_segment_management.py [-h] [-v] [-q] [-l] [-g SEGMENT_ID] [-d SEGMENT_ID] [--add] [--update SEGMENT_ID] [additional_args]

**Examples**:

List all Application Segments:
    $ python application_segment_management.py -l

Get details of a specific Application Segment by ID:
    $ python application_segment_management.py -g 99999

Delete an Application Segment by ID:
    $ python application_segment_management.py -d 99999

Add a new Application Segment:
    $ python application_segment_management.py --add --name "New App Segment" --domain_names example.com --segment_group_id 12345 --server_group_ids 67890 --tcp_port_ranges 80,80 --udp_port_ranges 1000,1000

Update an existing Application Segment:
    $ python application_segment_management.py --update 99999 --name "Updated App Segment" --description "Updated description"

"""

from zscaler import ZPAClientHelper
import argparse
import logging
import json
import os
from zscaler.utils import str2bool


def main():
    parser = argparse.ArgumentParser(description="Manage Application Segments for Zscaler Private Access (ZPA).")
    # Existing arguments
    parser.add_argument("-v", "--verbose", action="count", help="Verbose (-vv for extra verbose)")
    parser.add_argument("-q", "--quiet", action="store_true", help="Suppress all output")
    parser.add_argument("-l", "--list", action="store_true", help="List all application segments")
    parser.add_argument(
        "-g",
        "--get",
        metavar="SEGMENT_ID",
        help="Get details of an application segment by ID",
    )
    parser.add_argument(
        "-d",
        "--delete",
        metavar="SEGMENT_ID",
        help="Delete an application segment by ID",
    )
    parser.add_argument("--add", action="store_true", help="Add a new application segment")
    parser.add_argument("--update", metavar="SEGMENT_ID", help="Update an existing application segment")

    # New arguments for adding/updating segments
    parser.add_argument("--name", help="The name of the application segment")
    parser.add_argument("--enabled", type=str2bool, help="Whether the Application Segment is enabled")
    parser.add_argument(
        "--domain_names",
        nargs="+",
        help="List of domain names or IP addresses for the application segment",
    )
    parser.add_argument(
        "--segment_group_id",
        help="The unique identifier for the segment group this application segment belongs to",
    )
    parser.add_argument(
        "--server_group_ids",
        nargs="+",
        help="The list of server group IDs that belong to this application segment",
    )
    parser.add_argument(
        "--tcp_port_ranges",
        nargs="+",
        help="List of TCP port ranges, e.g., '80,80' '443,443'",
    )
    parser.add_argument(
        "--udp_port_ranges",
        nargs="+",
        help="List of UDP port ranges, e.g., '1000,1000' '2000,2000'",
    )

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
        app_segments = client.app_segments.list_segments()
        print(json.dumps(app_segments, indent=4))

    elif args.get:
        app_segment = client.app_segments.get_segment(args.get)
        print(json.dumps(app_segment, indent=4) if app_segment else f"No application segment found with ID {args.get}")

    elif args.delete:
        response_code = client.app_segments.delete_segment(args.delete)
        if response_code == 204:
            print(f"Application segment {args.delete} deleted successfully.")
        else:
            print(f"Failed to delete application segment {args.delete}. Response code: {response_code}")

    elif args.add:
        # Gather additional details required for adding an application segment
        # For simplicity, using placeholder values
        name = "New App Segment"
        domain_names = ["example.com"]
        segment_group_id = "12345"
        server_group_ids = ["67890"]
        tcp_port_ranges = [("80", "80")]
        udp_port_ranges = [("1000", "1000")]
        app_segment = client.app_segments.add_segment(
            name=name,
            domain_names=domain_names,
            segment_group_id=segment_group_id,
            server_group_ids=server_group_ids,
            tcp_port_ranges=tcp_port_ranges,
            udp_port_ranges=udp_port_ranges,
        )
        print(f"Application segment added successfully: {app_segment}")

    elif args.update:
        # Gather details required for updating an application segment
        # For simplicity, using placeholder values for update
        update_fields = {
            "name": "Updated App Segment",
            "description": "Updated description",
        }
        app_segment = client.app_segments.update_segment(segment_id=args.update, **update_fields)
        print(f"Application segment {args.update} updated successfully: {app_segment}")


if __name__ == "__main__":
    main()
