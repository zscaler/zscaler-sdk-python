#!/usr/bin/env python

"""
zdx_web_probes_cli.py
=====================

CLI tool to interact with ZDX Devices API to fetch web probes.

**Usage**::

    zdx_web_probes_cli.py [--use-legacy-client]

**Examples**:

List all active web probes for a device and application:
    $ python3 zdx_web_probes_cli.py

Using Legacy Client:
    $ python3 zdx_web_probes_cli.py --use-legacy-client

"""

import os
import logging
import argparse
from prettytable import PrettyTable
from zscaler import ZscalerClient
from zscaler.oneapi_client import LegacyZDXClient


def prompt_for_input(prompt_message, required=True):
    while True:
        user_input = input(prompt_message).strip()
        if user_input or not required:
            return user_input
        print("This field is required.")


def prompt_for_since():
    try:
        since_input = input("Enter the number of hours to look back (optional): ").strip()
        if since_input:
            return int(since_input)
        else:
            return None  # Optional field
    except ValueError as e:
        print(f"Invalid input: {e}")
        return None


def display_table(data, headers):
    if not data:
        print("No data available.")
        return

    table = PrettyTable(headers)
    table.align = "l"

    for row in data:
        table.add_row(row)
    print(table)


def extract_web_probes_data(probes):
    extracted_data = []
    for probe in probes:
        probe_id = probe.get("id")
        name = probe.get("name")
        avg_pft = probe.get("avg_pft")
        num_probes = probe.get("num_probes")
        avg_score = probe.get("avg_score")
        extracted_data.append([probe_id, name, avg_pft, num_probes, avg_score])
    return extracted_data


def main():
    parser = argparse.ArgumentParser(description="Interact with ZDX Devices API to fetch web probes")
    parser.add_argument("--use-legacy-client", action="store_true", help="Use legacy ZDX client instead of OneAPI client")
    args = parser.parse_args()

    # Set up logging
    logging.basicConfig(level=logging.DEBUG)

    # Initialize client based on the flag
    if args.use_legacy_client:
        # Legacy client configuration
        ZDX_CLIENT_ID = os.getenv("ZDX_CLIENT_ID")
        ZDX_CLIENT_SECRET = os.getenv("ZDX_CLIENT_SECRET")
        
        if not ZDX_CLIENT_ID or not ZDX_CLIENT_SECRET:
            print("Error: ZDX_CLIENT_ID and ZDX_CLIENT_SECRET environment variables are required for legacy client.")
            return

        config = {
            "key_id": ZDX_CLIENT_ID,
            "key_secret": ZDX_CLIENT_SECRET,
        }
        
        client = LegacyZDXClient(config)
    else:
        # OneAPI client configuration
        ZSCALER_CLIENT_ID = os.getenv("ZSCALER_CLIENT_ID")
        ZSCALER_CLIENT_SECRET = os.getenv("ZSCALER_CLIENT_SECRET")
        ZSCALER_VANITY_DOMAIN = os.getenv("ZSCALER_VANITY_DOMAIN")
        
        if not ZSCALER_CLIENT_ID or not ZSCALER_CLIENT_SECRET:
            print("Error: ZSCALER_CLIENT_ID and ZSCALER_CLIENT_SECRET environment variables are required for OneAPI client.")
            return

        config = {
            'clientId': ZSCALER_CLIENT_ID,
            'clientSecret': ZSCALER_CLIENT_SECRET,
        }
        
        # Add vanity domain if provided
        if ZSCALER_VANITY_DOMAIN:
            config['vanityDomain'] = ZSCALER_VANITY_DOMAIN
        
        client = ZscalerClient(config)

    # Prompt the user for device ID and app ID
    device_id = prompt_for_input("Enter the device ID: ")
    app_id = prompt_for_input("Enter the app ID: ")
    since = prompt_for_since()

    # Prepare query parameters
    query_params = {}
    if since:
        query_params["since"] = since

    # Call the API to get web probes
    try:
        web_probes, _, err = client.zdx.devices.get_web_probes(device_id, app_id, query_params=query_params)
        if err:
            print(f"Error retrieving web probes: {err}")
            return
        
        # Convert to list of dictionaries for display
        probes_data = []
        for probe in web_probes:
            if hasattr(probe, 'as_dict'):
                probes_data.append(probe.as_dict())
            else:
                probes_data.append(probe)
        
        headers = ["ID", "Name", "Avg PFT", "Num Probes", "Avg Score"]
        data = extract_web_probes_data(probes_data)
        display_table(data, headers)
    except Exception as e:
        print(f"An error occurred while fetching web probes: {e}")


if __name__ == "__main__":
    main()
