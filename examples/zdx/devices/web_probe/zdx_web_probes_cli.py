#!/usr/bin/env python

"""
zdx_web_probes_cli.py
=====================

CLI tool to interact with ZDX Devices API to fetch web probes.

**Usage**::

    zdx_web_probes_cli.py

**Examples**:

List all active web probes for a device and application:
    $ python3 zdx_web_probes_cli.py

"""

import os
import logging
import argparse
from prettytable import PrettyTable
from zscaler.zdx import ZDXClientHelper
from zscaler.zdx.devices import DevicesAPI


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

    # Prompt the user for device ID and app ID
    device_id = prompt_for_input("Enter the device ID: ")
    app_id = prompt_for_input("Enter the app ID: ")
    since = prompt_for_since()

    # Prepare keyword arguments
    kwargs = {
        "since": since,
    }

    # Remove None values from kwargs
    kwargs = {k: v for k, v in kwargs.items() if v is not None}

    # Call the API to get web probes
    try:
        web_probes = devices_api.get_web_probes(device_id, app_id, **kwargs)
        headers = ["ID", "Name", "Avg PFT", "Num Probes", "Avg Score"]
        data = extract_web_probes_data(web_probes)
        display_table(data, headers)
    except Exception as e:
        print(f"An error occurred while fetching web probes: {e}")


if __name__ == "__main__":
    main()
