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
vip_group_by_datacenter.py
=======================

Returns a list of recommended GRE tunnel (VIPs) grouped by data center in Zscaler Internet Access (ZIA).

Usage:
    python3 vip_group_by_datacenter.py --source_ip <SOURCE_IP> [--routable_ip] [--within_country_only] [--include_private_service_edge] [--include_current_vips] [--latitude <LATITUDE>] [--longitude <LONGITUDE>] [--geo_override]

Options:
    --source_ip                    The source IP address to get recommended VIPs for.
    --routable_ip                  Specify to include routable IPs. Default is True.
    --within_country_only          Restrict search within the same country. Default is False.
    --include_private_service_edge Include ZIA Private Service Edge VIPs. Default is True.
    --include_current_vips         Include currently assigned VIPs. Default is True.
    --latitude                     Latitude coordinate of GRE tunnel source.
    --longitude                    Longitude coordinate of GRE tunnel source.
    --geo_override                 Override the geographic coordinates. Default is False.

Examples:
    python3 vip_group_by_datacenter.py --source_ip 203.0.113.30
    python3 vip_group_by_datacenter.py --source_ip 203.0.113.30 --routable_ip False --within_country_only True
"""

import argparse
import os
from zscaler import ZIAClientHelper
import json


def main():
    parser = argparse.ArgumentParser(
        description="Returns a list of Recommended Virtual IP Addresses (VIPs) grouped by data center in Zscaler Internet Access (ZIA)."
    )
    parser.add_argument(
        "--source_ip",
        required=True,
        help="The source IP address to get recommended VIPs for.",
    )
    parser.add_argument(
        "--routable_ip",
        type=bool,
        default=True,
        help="Specify to include routable IPs. Default is True.",
    )
    parser.add_argument(
        "--within_country_only",
        type=bool,
        default=False,
        help="Restrict search within the same country. Default is False.",
    )
    parser.add_argument(
        "--include_private_service_edge",
        type=bool,
        default=True,
        help="Include ZIA Private Service Edge VIPs. Default is True.",
    )
    parser.add_argument(
        "--include_current_vips",
        type=bool,
        default=True,
        help="Include currently assigned VIPs. Default is True.",
    )
    parser.add_argument("--latitude", type=str, help="Latitude coordinate of GRE tunnel source.")
    parser.add_argument("--longitude", type=str, help="Longitude coordinate of GRE tunnel source.")
    parser.add_argument(
        "--geo_override",
        type=bool,
        default=False,
        help="Override the geographic coordinates. Default is False.",
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

    # Prepare kwargs from args
    kwargs = {
        "routable_ip": args.routable_ip,
        "within_country_only": args.within_country_only,
        "include_private_service_edge": args.include_private_service_edge,
        "include_current_vips": args.include_current_vips,
        "latitude": args.latitude,
        "longitude": args.longitude,
        "geo_override": args.geo_override,
    }

    # Fetch VIP groups by data center
    vip_groups = zia.traffic.list_vip_group_by_dc(source_ip=args.source_ip, **kwargs)
    if vip_groups:
        print("VIP groups by data center:")
        print(json.dumps([vip.to_dict() for vip in vip_groups], indent=4))
    else:
        print("Failed to fetch VIP groups by data center. No response or error received.")


if __name__ == "__main__":
    main()
