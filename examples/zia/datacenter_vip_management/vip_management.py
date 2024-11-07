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
vip_management.py
=================

Returns a list of Virtual IP Addresses (VIPs) in Zscaler Internet Access (ZIA).

Usage:
    python vip_management.py [options]

Options:
    --get_all_vips                List all VIPs including public and private.
    --get_all_public_vips         List all public VIPs.
    --get_all_private_vips        List all private VIPs.

Examples:
    List all VIPs including public and private:
        $ python3 vip_management.py --get_all_vips

    List all public VIPs:
        $ python3 vip_management.py --get_all_public_vips

    List all private VIPs:
        $ python3 vip_management.py --get_all_private_vips
"""

import argparse
import json
import os
from zscaler import ZIAClientHelper


def main():
    parser = argparse.ArgumentParser(description="Manages VIPs in ZIA.")
    parser.add_argument(
        "--get_all_vips",
        action="store_true",
        help="List all VIPs including public and private.",
    )
    parser.add_argument("--get_all_public_vips", action="store_true", help="List all public VIPs.")
    parser.add_argument("--get_all_private_vips", action="store_true", help="List all private VIPs.")
    args = parser.parse_args()

    # Initialize ZIAClientHelper
    print("\n\n ##########  STARTING SDK ##########\n\n")
    ZIA_USERNAME = os.getenv("ZIA_USERNAME")
    ZIA_PASSWORD = os.getenv("ZIA_PASSWORD")
    ZIA_API_KEY = os.getenv("ZIA_API_KEY")
    ZIA_CLOUD = os.getenv("ZIA_CLOUD")

    client = ZIAClientHelper(
        username=ZIA_USERNAME,
        password=ZIA_PASSWORD,
        api_key=ZIA_API_KEY,
        cloud=ZIA_CLOUD,
    )

    if args.get_all_vips:
        list_vips(client, include="all")
    elif args.get_all_public_vips:
        list_vips(client, include="public")
    elif args.get_all_private_vips:
        list_vips(client, include="private")


def list_vips(client, include):
    params = {"include": include}  # Define params as a dict
    vips = client.traffic.list_vips(params=params)  # Pass params dict directly
    print(json.dumps(vips, indent=4) if vips else f"No VIPs found for the specified type: {include}.")


if __name__ == "__main__":
    main()
