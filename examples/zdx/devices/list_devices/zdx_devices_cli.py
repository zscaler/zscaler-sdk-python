#!/usr/bin/env python

"""
zdx_devices_cli.py
====================

CLI tool to interact with ZDX Devices API.

**Usage**::

    zdx_devices_cli.py [--use-legacy-client]

**Examples**:

List all devices:
    $ python3 zdx_devices_cli.py

List devices for the past 24 hours:
    $ python3 zdx_devices_cli.py --since 24

List devices for a specific location:
    $ python3 zdx_devices_cli.py --location_id 12345

Using Legacy Client:
    $ python3 zdx_devices_cli.py --use-legacy-client

"""

import os
import logging
import argparse
from prettytable import PrettyTable
from zscaler import ZscalerClient
from zscaler.oneapi_client import LegacyZDXClient
from box import BoxList


def prompt_for_input(prompt_message, required=True):
    while True:
        user_input = input(prompt_message).strip()
        if user_input or not required:
            return user_input
        print("This field is required.")


def display_table(data, headers):
    if not data:
        print("No data available.")
        return

    table = PrettyTable(headers)

    # Set column alignments
    table.align["ID"] = "r"
    table.align["Name"] = "l"
    table.align["User ID"] = "r"

    for row in data:
        table.add_row(row)
    print(table)


def extract_devices_data(devices):
    extracted_data = []
    for device in devices:
        device_id = device.get("id")
        name = device.get("name")
        userid = device.get("userid")
        extracted_data.append([device_id, name, userid])
    return extracted_data


def main():
    parser = argparse.ArgumentParser(description="Interact with ZDX Devices API")
    parser.add_argument("--since", type=int, help="The number of hours to look back for devices")
    parser.add_argument("--location_id", type=str, help="The unique ID for the location")
    parser.add_argument("--department_id", type=str, help="The unique ID for the department")
    parser.add_argument("--geo_id", type=str, help="The unique ID for the geolocation")
    parser.add_argument("--user_ids", type=str, nargs="+", help="List of user IDs")
    parser.add_argument("--emails", type=str, nargs="+", help="List of email addresses")
    parser.add_argument("--mac_address", type=str, help="MAC address of the device")
    parser.add_argument("--private_ipv4", type=str, help="Private IPv4 address of the device")
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

    # Prepare query parameters
    query_params = {}
    if args.since:
        query_params["since"] = args.since
    if args.location_id:
        query_params["location_id"] = args.location_id
    if args.department_id:
        query_params["department_id"] = args.department_id
    if args.geo_id:
        query_params["geo_id"] = args.geo_id
    if args.user_ids:
        query_params["user_ids"] = args.user_ids
    if args.emails:
        query_params["emails"] = args.emails
    if args.mac_address:
        query_params["mac_address"] = args.mac_address
    if args.private_ipv4:
        query_params["private_ipv4"] = args.private_ipv4

    # Call the API to list devices
    try:
        devices, _, err = client.zdx.devices.list_devices(query_params=query_params)
        if err:
            print(f"Error listing devices: {err}")
            return
        
        # Convert to list of dictionaries for display
        devices_data = []
        for device in devices:
            if hasattr(device, 'as_dict'):
                devices_data.append(device.as_dict())
            else:
                devices_data.append(device)
        
        headers = ["ID", "Name", "User ID"]
        data = extract_devices_data(devices_data)
        display_table(data, headers)
    except Exception as e:
        print(f"An error occurred while fetching devices: {e}")


if __name__ == "__main__":
    main()
