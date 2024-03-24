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
add_ipsec_fqdn_location_gw_options.py
=================================

This script interacts with the Zscaler Internet Access (ZIA) API to manage locations. It supports adding a location with an associated IPSec tunnel (UFQDN type) and automatically activates changes.

Usage:
    python3 add_ipsec_fqdn_location_gw_options.py --add_location --name "Location Name" --email "user@example.com" --pre_shared_key "YourPreSharedKey" --gateway_options

Please ensure that environment variables for ZIA_USERNAME, ZIA_PASSWORD, ZIA_API_KEY, and ZIA_CLOUD are set before running this script.
"""

import argparse
import json
import os
import time
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
        gateway_options["idleTimeInMinutes"] = int(input("Set Idle Time in Minutes for Surrogate IP (e.g., 30): ").strip() or "30")
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

def add_location_with_ufqdn_tunnel(zia, name, email, pre_shared_key, gateway_options):
    print("\nCreating IPSec UFQDN tunnel...")
    vpn_credential = zia.traffic.add_vpn_credential(
        authentication_type="UFQDN",
        fqdn=email,
        pre_shared_key=pre_shared_key
    )
    vpn_credential_id = vpn_credential.get('id')
    print(f"IPSec UFQDN tunnel created with ID: {vpn_credential_id}")

    print(f"\nAdding location '{name}' with associated IPSec UFQDN tunnel...")
    location = zia.locations.add_location(
        name=name,
        vpn_credentials=[{'id': vpn_credential_id, 'type': 'UFQDN'}],
        **gateway_options
    )
    print("Location added successfully:", json.dumps(location, indent=4))

    print("\nActivating configuration changes...")
    time.sleep(5)  # Delay for 5 seconds before activating
    activation_status = zia.activate.activate()
    print("Configuration changes activated successfully. Status:", activation_status)

def main():
    parser = argparse.ArgumentParser(description="Manage locations in Zscaler Internet Access with an associated IPSec tunnel (UFQDN type).")
    parser.add_argument("--add_location", action="store_true", help="Add a new location with an IPSec UFQDN tunnel.")
    parser.add_argument("--name", help="Name of the location to add.")
    parser.add_argument("--email", help="Email address for the IPSec tunnel (UFQDN).")
    parser.add_argument("--pre_shared_key", help="Pre-shared key for the IPSec tunnel. If not provided, a random one will be generated.")

    args = parser.parse_args()

    if args.add_location and args.name and args.email:
        zia = ZIAClientHelper(
            username=os.getenv("ZIA_USERNAME"),
            password=os.getenv("ZIA_PASSWORD"),
            api_key=os.getenv("ZIA_API_KEY"),
            cloud=os.getenv("ZIA_CLOUD")
        )

        gateway_options = prompt_for_gateway_options()

        add_location_with_ufqdn_tunnel(zia, args.name, args.email, args.pre_shared_key, gateway_options)
    else:
        print("Missing required arguments: --name and --email are required for adding a location")

if __name__ == "__main__":
    main()
