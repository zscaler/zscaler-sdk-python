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
add_ipsec_fqdn_location_sublocations.py
=================================

This script provides a CLI tool for managing sublocations in Zscaler Internet Access (ZIA). It facilitates the addition of a sublocation, which is a logical division within a parent location. This can be particularly useful for organizations with multiple office branches or networks within a larger network. The script supports configuring various gateway options for the sublocation, provided the --gateway_options flag is set. After the sublocation and its configurations are defined, the script automatically activates the configuration changes.

Usage:
    python3 add_ipsec_fqdn_location_sublocations.py --add_sublocation --name "Sublocation Name" --parent "Parent Location Name or ID" --ip_range "IP Address Range" [--gateway_options]

Options:
    --add_sublocation    Flag to indicate the addition of a new sublocation.
    --name               Required. The name of the sublocation to be added.
    --parent             Required. The parent location's name or ID under which the sublocation will be added.
    --ip_range           Required. The IP address range for the sublocation, specified in CIDR notation or as an IP range.
    --gateway_options    Optional. Flag to prompt for configuring various gateway options for the sublocation.

Please ensure that the following environment variables are set before running the script:
    ZIA_USERNAME - The username for ZIA.
    ZIA_PASSWORD - The password for ZIA.
    ZIA_API_KEY  - The API Key for ZIA.
    ZIA_CLOUD    - The ZIA Cloud URL.

The script will prompt the user to configure various gateway options if the --gateway_options flag is provided. These options include enabling authentication, SSL inspection, Zscaler App SSL Setting, firewall, IPS control, AUP, and Surrogate IP among others.

Examples:
    To add a new sublocation named 'Marketing Department' under the parent location 'Headquarters' with an IP range '192.168.1.0/24', without configuring additional gateway options:
    python3 add_ipsec_fqdn_location_sublocations.py --add_sublocation --name "Marketing Department" --parent "Headquarters" --ip_range "192.168.1.0/24"

    To add a new sublocation with additional gateway options configured, append the --gateway_options flag:
    python3 add_ipsec_fqdn_location_sublocations.py --add_sublocation --name "Engineering Department" --parent "Headquarters" --ip_range "192.168.2.0/24" --gateway_options
"""

import argparse
import json
import os
import time
from zscaler import ZIAClientHelper


def get_location_id_by_name(zia, location_name):
    """Get location ID by location name."""
    location = zia.locations.get_location(location_name=location_name)
    if location:
        return location.id
    else:
        raise ValueError(f"Location with name '{location_name}' not found.")


def prompt_for_gateway_options():
    print("\nConfiguring gateway options for the location...")
    gateway_options = {
        "auth_required": prompt_yes_no("Enable Authentication (auth_required)?"),
        "ssl_scan_enabled": prompt_yes_no("Enable SSL Inspection (ssl_scan_enabled)?"),
        "zapp_ssl_scan_enabled": prompt_yes_no("Enable Zscaler App SSL Setting (zapp_ssl_scan_enabled)?"),
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


def add_sublocation(zia, name, parent_id_or_name, ip_range, gateway_options):
    # Determine if parent_id_or_name is an ID or a name
    try:
        parent_id = int(parent_id_or_name)
    except ValueError:
        # If conversion fails, assume it's a name and query for the ID
        parent_id = get_location_id_by_name(zia, parent_id_or_name)

    print(f"\nAdding Sublocation '{name}' under parent ID: {parent_id}...")
    sublocation_response = zia.locations.add_location(
        name=name, parent_id=parent_id, ip_addresses=[ip_range], **gateway_options
    )
    print("Sublocation added successfully:", json.dumps(sublocation_response, indent=4))
    print("\nActivating configuration changes...")
    time.sleep(5)  # Delay for 5 seconds before activating
    activation_status = zia.activate.activate()
    print("Configuration changes activated successfully. Status:", activation_status)


def main():
    parser = argparse.ArgumentParser(description="Add a sublocation to Zscaler Internet Access.")
    parser.add_argument("--add_sublocation", action="store_true", help="Add a new sublocation.")
    parser.add_argument("--name", required=True, help="Name of the sublocation to add.")
    parser.add_argument("--parent", required=True, help="Parent location name or ID.")
    parser.add_argument("--ip_range", required=True, help="IP address range for the sublocation.")
    parser.add_argument("--gateway_options", action="store_true", help="Prompt for gateway options.")

    args = parser.parse_args()

    if args.add_sublocation:
        zia = ZIAClientHelper(
            username=os.getenv("ZIA_USERNAME"),
            password=os.getenv("ZIA_PASSWORD"),
            api_key=os.getenv("ZIA_API_KEY"),
            cloud=os.getenv("ZIA_CLOUD"),
        )
        gateway_options = prompt_for_gateway_options() if args.gateway_options else {}
        add_sublocation(zia, args.name, args.parent, args.ip_range, gateway_options)
    else:
        print("Missing required arguments for adding a sublocation.")


if __name__ == "__main__":
    main()
