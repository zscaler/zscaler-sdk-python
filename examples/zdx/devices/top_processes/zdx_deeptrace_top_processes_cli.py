#!/usr/bin/env python

"""
zdx_deeptrace_top_processes_cli.py
==================================

CLI tool to interact with ZDX Devices API to fetch deeptrace top processes.

**Usage**::

    zdx_deeptrace_top_processes_cli.py [--use-legacy-client]

**Examples**:

Get top processes for a deeptrace:
    $ python3 zdx_deeptrace_top_processes_cli.py

Using Legacy Client:
    $ python3 zdx_deeptrace_top_processes_cli.py --use-legacy-client

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


def display_table(data, headers):
    if not data:
        print("No data available.")
        return

    table = PrettyTable(headers)
    table.align = "l"

    for row in data:
        table.add_row(row)
    print(table)


def extract_top_processes_data(processes):
    extracted_data = []
    for category in processes:
        category_name = category.get("category")
        unit = category.get("unit")
        proc_list = category.get("processes", [])

        for process in proc_list:
            process_name = process.get("name")
            process_id = process.get("id")
            extracted_data.append([category_name, unit, process_name, process_id])
    return extracted_data


def main():
    parser = argparse.ArgumentParser(description="Interact with ZDX Devices API to fetch deeptrace top processes")
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

    # Prompt the user for device ID and trace ID
    device_id = prompt_for_input("Enter the device ID: ")
    trace_id = prompt_for_input("Enter the trace ID: ")

    # Call the API to get top processes
    try:
        top_processes, _, err = client.zdx.devices.get_deeptrace_top_processes(device_id, trace_id)
        if err:
            print(f"Error retrieving deeptrace top processes: {err}")
            return
        
        if hasattr(top_processes, 'as_dict'):
            top_processes_dict = top_processes.as_dict()
        else:
            top_processes_dict = top_processes
        
        headers = ["Category", "Unit", "Process Name", "Process ID"]
        data = extract_top_processes_data(top_processes_dict)
        display_table(data, headers)
    except Exception as e:
        print(f"An error occurred while fetching deeptrace top processes: {e}")


if __name__ == "__main__":
    main()
