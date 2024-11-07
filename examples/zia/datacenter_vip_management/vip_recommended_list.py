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
vip_recommended_list.py
=======================

Returns a list of Recommended Virtual IP Addresses (VIPs) in Zscaler Internet Access (ZIA).

Usage:
    python3 vip_recommended_list.py --source_ip <SOURCE_IP> [--closest_diverse]

Options:
    --source_ip        The source IP address to get recommended VIPs for.
    --closest_diverse  Retrieve the closest diverse VIP IDs along with detailed information.

Examples:
    python3 vip_recommended_list.py --source_ip 1.1.1.1
    python3 vip_recommended_list.py --source_ip 1.1.1.1 --closest_diverse
"""

import argparse
import os
from zscaler import ZIAClientHelper
import json


def main():
    parser = argparse.ArgumentParser(
        description="Returns a list of Recommended Virtual IP Addresses (VIPs) in Zscaler Internet Access (ZIA)."
    )
    parser.add_argument(
        "--source_ip",
        required=True,
        help="The source IP address to get recommended VIPs for.",
    )
    parser.add_argument(
        "--closest_diverse",
        action="store_true",
        help="Retrieve the closest diverse VIP IDs along with detailed information.",
    )

    args = parser.parse_args()

    # Initialize ZIAClientHelper
    ZIA_USERNAME = os.getenv("ZIA_USERNAME")
    ZIA_PASSWORD = os.getenv("ZIA_PASSWORD")
    ZIA_API_KEY = os.getenv("ZIA_API_KEY")
    ZIA_CLOUD = os.getenv("ZIA_CLOUD")

    zia = ZIAClientHelper(
        username=ZIA_USERNAME,
        password=ZIA_PASSWORD,
        api_key=ZIA_API_KEY,
        cloud=ZIA_CLOUD,
    )

    if args.closest_diverse:
        # Call get_closest_diverse_vip_ids method
        preferred_vip_id, secondary_vip_id = zia.traffic.get_closest_diverse_vip_ids(ip_address=args.source_ip)

        # Fetch the complete list again to extract detailed information
        vips = zia.traffic.list_vips_recommended(source_ip=args.source_ip)
        vip_details = {}
        for vip in vips:
            if vip.id in [preferred_vip_id, secondary_vip_id]:
                vip_details[str(vip.id)] = vip.to_dict()

        # Print detailed information for preferred and secondary VIPs in JSON format
        print(json.dumps(vip_details, indent=4))
    else:
        # Call list_vips_recommended method
        vips = zia.traffic.list_vips_recommended(source_ip=args.source_ip)
        for vip in vips:
            # Convert Box object to dictionary
            vip_dict = vip.to_dict()
            # Print in JSON format
            print(json.dumps(vip_dict, indent=4))


if __name__ == "__main__":
    main()
