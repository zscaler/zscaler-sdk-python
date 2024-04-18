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
add_ipsec_ip_location_gw_options.py
====================================

This Python script is designed as a command-line interface (CLI) tool to facilitate the addition of new locations within the Zscaler Internet Access (ZIA) environment, specifically focusing on locations associated with an IPSec tunnel using IP authentication type. It leverages the ZIA Python SDK to communicate with the ZIA API, allowing for streamlined operations such as creating static IPs, configuring VPN credentials, adding locations, and enabling various gateway options based on user input.

Requirements:
    - Zscaler Python SDK must be installed and accessible in the script's environment.
    - User must have valid credentials with sufficient permissions to interact with the ZIA API.
    - The environment variables `ZIA_USERNAME`, `ZIA_PASSWORD`, `ZIA_API_KEY`, and `ZIA_CLOUD` must be properly set up prior to executing the script.

Usage:
    python3 add_ipsec_ip_location_gw_options.py --add_location --name <LOCATION_NAME> --ip_address <STATIC_IP> --pre_shared_key <PSK> [--gateway_options]

Arguments:
    --add_location       Signals the script to proceed with the creation of a new location associated with an IPSec IP tunnel.
    --name <LOCATION_NAME>   Specifies the name for the new location being added.
    --ip_address <STATIC_IP> Specifies the static IP address to be used for the IPSec tunnel.
    --pre_shared_key <PSK>   Optional. Specifies the pre-shared key for the IPSec tunnel. If omitted, a random key will be generated.
    --gateway_options        Optional flag. When set, the script will prompt the user to configure various gateway options for the new location.

Features:
    - Dynamic prompting for gateway configuration options if the --gateway_options flag is provided. Allows the user to enable or disable specific features such as authentication, SSL inspection, firewall, and more for the new location.
    - Automatic activation of configuration changes once the new location and associated settings have been successfully created.
    - Validation checks to ensure required parameters are provided and to guide the user through the configuration process effectively.

Examples:
    Adding a location without gateway options:
        python3 add_ipsec_ip_location_gw_options.py --add_location --name "San Francisco Office" --ip_address "203.0.113.10" --pre_shared_key "mySecretPSK"
    
    Adding a location with gateway options:
        python3 add_ipsec_ip_location_gw_options.py --add_location --name "San Francisco Office" --ip_address "203.0.113.10" --pre_shared_key "mySecretPSK" --gateway_options

Note:
    This script assumes that the ZIA environment is correctly configured and that the necessary environment variables are set. For detailed documentation on the ZIA API and the Python SDK, please refer to the official Zscaler documentation.
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
        if response == "y":
            return True
        elif response == "n":
            return False


def add_location_with_ip_tunnel(zia, name, ip_address, pre_shared_key, gateway_options):
    print("\nCreating Static IP...")
    static_ip_response = zia.traffic.add_static_ip(ip_address=ip_address)
    print(f"Static IP {ip_address} created successfully. Response: {json.dumps(static_ip_response, indent=4)}")

    # Now create VPN credential with Static IP
    print("\nCreating IPSec IP tunnel...")
    vpn_credential_response = zia.traffic.add_vpn_credential(
        authentication_type="IP", ip_address=ip_address, pre_shared_key=pre_shared_key
    )
    print(
        f"IPSec IP tunnel created with ID: {vpn_credential_response.get('id')} Response: {json.dumps(vpn_credential_response, indent=4)}"
    )

    # Preparing vpn_credentials format for the location
    vpn_credentials_formatted = [
        {
            "id": vpn_credential_response.get("id"),
            "type": "IP",
            "ipAddress": ip_address,  # Ensure the ipAddress key is correctly included
        }
    ]

    # Finally, add the location with the VPN credential and the static IP address
    print(f"\nAdding location '{name}' with associated IPSec IP tunnel...")
    location_response = zia.locations.add_location(
        name=name,
        ip_addresses=[ip_address],  # Include the static IP address in the list
        vpn_credentials=vpn_credentials_formatted,
        **gateway_options,
    )
    print("Location added successfully:", json.dumps(location_response, indent=4))

    print("\nActivating configuration changes...")
    time.sleep(5)  # Delay for 5 seconds before activating
    activation_status = zia.activate.activate()
    print("Configuration changes activated successfully. Status:", activation_status)


def main():
    parser = argparse.ArgumentParser(
        description="Manage locations in Zscaler Internet Access with an associated IPSec tunnel (IP type)."
    )
    parser.add_argument(
        "--add_location",
        action="store_true",
        help="Add a new location with an IPSec IP tunnel.",
    )
    parser.add_argument("--name", required=True, help="Name of the location to add.")
    parser.add_argument("--ip_address", required=True, help="The IP address for the IPSec tunnel.")
    parser.add_argument(
        "--pre_shared_key",
        help="Pre-shared key for the IPSec tunnel. If not provided, a random one will be generated.",
    )
    parser.add_argument("--gateway_options", action="store_true", help="Prompt for gateway options.")

    args = parser.parse_args()

    if args.add_location and args.name and args.ip_address:
        zia = ZIAClientHelper(
            username=os.getenv("ZIA_USERNAME"),
            password=os.getenv("ZIA_PASSWORD"),
            api_key=os.getenv("ZIA_API_KEY"),
            cloud=os.getenv("ZIA_CLOUD"),
        )
        if args.gateway_options:
            gateway_options = prompt_for_gateway_options()
        else:
            gateway_options = {}

        add_location_with_ip_tunnel(zia, args.name, args.ip_address, args.pre_shared_key, gateway_options)
    else:
        print(
            "Missing required arguments: --name and --ip_address are required for adding a location with an IPSec IP tunnel."
        )


if __name__ == "__main__":
    main()
