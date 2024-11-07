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
add_static_and_gre_tunnel.py
=============================

This script is designed to automate the creation of a GRE tunnel in Zscaler Internet Access (ZIA) by first creating a static IP and then using it to establish a GRE tunnel with the closest data center VIPs, finally creating a location associated with this tunnel.

Usage:
    python3 add_static_and_gre_tunnel.py --ip_address <STATIC_IP> --location_name <LOCATION_NAME> [--comments <COMMENTS>]

Options:
    --ip_address     The static public IP address to be added and used as the source IP for the GRE tunnel.
    --location_name  The name of the new location associated with the GRE tunnel.
    --comments       Optional. Comments or additional information about the GRE tunnel.

Please ensure that the following environment variables are set before running the script:
    ZIA_USERNAME - The username for ZIA.
    ZIA_PASSWORD - The password for ZIA.
    ZIA_API_KEY  - The API Key for ZIA.
    ZIA_CLOUD    - The ZIA Cloud URL.

Examples:
    python3 add_static_and_gre_tunnel.py --ip_address "203.0.113.10" --location_name "New Office Location"

Please ensure that ZIA credentials and the cloud URL are correctly set as environment variables before running this script.
"""

import argparse
import json
import os
from zscaler import ZIAClientHelper


def prompt_for_gateway_options():
    print("\nConfiguring gateway options for the location...")
    gateway_options = {
        "auth_required": prompt_yes_no("Enable Authentication (auth_required)?"),
        "ssl_scan_enabled": prompt_yes_no("Enable SSL Inspection (ssl_scan_enabled)?"),
        "zapp_ssl_scan_enabled": prompt_yes_no("Enable Zscaler App SSL Setting (zapp_ssl_scan_enabled)?"),
        "xff_forward_enabled": prompt_yes_no("Enable XFF Forwarding (xff_forward_enabled)?"),
        "ofw_enabled": prompt_yes_no("Enable Firewall (ofw_enabled)?"),
        "ips_control": prompt_yes_no("Enable IPS Control (ips_control)?"),
        "aup_enabled": prompt_yes_no("Enable AUP (aup_enabled)?"),
        "surrogate_ip": prompt_yes_no("Enable Surrogate IP (surrogate_ip)?"),
    }

    if gateway_options["aup_enabled"]:
        gateway_options["aupTimeoutInDays"] = input("Set AUP Timeout in Days (at least 1): ").strip() or "1"

    if gateway_options["surrogate_ip"]:
        gateway_options["idleTimeInMinutes"] = int(
            input("Set Idle Time in Minutes for Surrogate IP (e.g., 30): ").strip() or "30"
        )
        gateway_options["displayTimeUnit"] = "MINUTE"
        if prompt_yes_no("Enforce Surrogate IP for Known Browsers (surrogateIPEnforcedForKnownBrowsers)?"):
            gateway_options["surrogateIPEnforcedForKnownBrowsers"] = True
            while True:
                refresh_time = int(input("Set Surrogate Refresh Time in Minutes (e.g., 480): ").strip() or "480")
                if refresh_time > gateway_options["idleTimeInMinutes"]:
                    print("Surrogate Refresh Time cannot be greater than Idle Time. Please enter a valid value.")
                else:
                    gateway_options["surrogateRefreshTimeInMinutes"] = refresh_time
                    break
            gateway_options["surrogateRefreshTimeUnit"] = "MINUTE"

    return gateway_options


def prompt_yes_no(question):
    """Simple Yes/No Prompt"""
    while True:
        response = input(f"{question} [y/n]: ").lower().strip()
        if response in ["y", "yes"]:
            return True
        elif response in ["n", "no"]:
            return False


def main():
    parser = argparse.ArgumentParser(description="CLI tool to add a GRE tunnel in Zscaler Internet Access.")
    parser.add_argument(
        "--ip_address",
        required=True,
        help="Static public IP address to add and use as source IP for the GRE tunnel.",
    )
    parser.add_argument("--location_name", required=True, help="Name for the new location.")
    parser.add_argument("--comments", help="Comments or additional information.")

    args = parser.parse_args()

    # Initialize ZIAClientHelper
    zia = ZIAClientHelper(
        username=os.getenv("ZIA_USERNAME"),
        password=os.getenv("ZIA_PASSWORD"),
        api_key=os.getenv("ZIA_API_KEY"),
        cloud=os.getenv("ZIA_CLOUD"),
    )

    # Prompt for configuring gateway options
    configure_gateway_options = prompt_yes_no("Would you like to configure gateway options for the location?")
    gateway_options = {}
    if configure_gateway_options:
        gateway_options = prompt_for_gateway_options()

    # Step 1: Create a static IP
    print("Proceeding to create a static IP...")
    static_ip_response = zia.traffic.add_static_ip(args.ip_address, comment=args.comments)
    print(f"Static IP created successfully: {json.dumps(static_ip_response, indent=4)}")

    # Step 2: Create GRE Tunnel
    print("Proceeding to create a GRE Tunnel...")
    gre_tunnel_response = zia.traffic.add_gre_tunnel(source_ip=args.ip_address, comment=args.comments)
    print(f"GRE Tunnel created successfully: {json.dumps(gre_tunnel_response, indent=4)}")

    # Step 3: Create Location with GRE Tunnel IP
    print("Proceeding to create a location...")
    location_response = zia.locations.add_location(
        name=args.location_name,
        ip_addresses=[args.ip_address],  # Associate the static IP with the location
        comments=args.comments,
        **gateway_options,
    )
    print(f"Location created successfully: {json.dumps(location_response, indent=4)}")

    # Activate configuration changes
    print("Activating configuration changes...")
    activation_status = zia.activate.activate()
    print(f"Configuration changes activated successfully. Status: {activation_status}")


if __name__ == "__main__":
    main()
