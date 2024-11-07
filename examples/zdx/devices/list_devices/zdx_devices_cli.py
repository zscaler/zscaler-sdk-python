#!/usr/bin/env python

"""
zdx_devices_cli.py
====================

CLI tool to interact with ZDX Devices API.

**Usage**::

    zdx_devices_cli.py

**Examples**:

List all devices:
    $ python3 zdx_devices_cli.py

List devices for the past 24 hours:
    $ python3 zdx_devices_cli.py --since 24

List devices for a specific location:
    $ python3 zdx_devices_cli.py --location_id 12345

"""

import os
import logging
import argparse
from prettytable import PrettyTable
from zscaler.zdx import ZDXClientHelper
from zscaler.zdx.devices import DevicesAPI
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

    args = parser.parse_args()

    # Set up logging
    logging.basicConfig(level=logging.DEBUG)

    # Initialize ZDXClientHelper
    ZDX_CLIENT_ID = os.getenv("ZDX_CLIENT_ID")
    ZDX_CLIENT_SECRET = os.getenv("ZDX_CLIENT_SECRET")

    client = ZDXClientHelper(
        client_id=ZDX_CLIENT_ID,
        client_secret=ZDX_CLIENT_SECRET,
    )

    devices_api = DevicesAPI(client)

    # Prepare keyword arguments
    kwargs = {
        "since": args.since,
        "location_id": args.location_id,
        "department_id": args.department_id,
        "geo_id": args.geo_id,
        "user_ids": args.user_ids,
        "emails": args.emails,
        "mac_address": args.mac_address,
        "private_ipv4": args.private_ipv4,
    }

    # Remove None values from kwargs
    kwargs = {k: v for k, v in kwargs.items() if v is not None}

    # Call the API to list devices
    try:
        devices_iterator = devices_api.list_devices(**kwargs)
        devices = list(devices_iterator)
        headers = ["ID", "Name", "User ID"]
        data = extract_devices_data(devices)
        display_table(data, headers)
    except Exception as e:
        print(f"An error occurred while fetching devices: {e}")


if __name__ == "__main__":
    main()
