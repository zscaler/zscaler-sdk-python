#!/usr/bin/env python

"""
zdx_deeptrace_top_processes_cli.py
==================================

CLI tool to interact with ZDX Devices API to fetch deeptrace top processes.

**Usage**::

    zdx_deeptrace_top_processes_cli.py

**Examples**:

Get top processes for a deeptrace:
    $ python3 zdx_deeptrace_top_processes_cli.py

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

    # Prompt the user for device ID and trace ID
    device_id = prompt_for_input("Enter the device ID: ")
    trace_id = prompt_for_input("Enter the trace ID: ")

    # Call the API to get top processes
    try:
        top_processes = devices_api.get_deeptrace_top_processes(device_id, trace_id)
        headers = ["Category", "Unit", "Process Name", "Process ID"]
        data = extract_top_processes_data(top_processes)
        display_table(data, headers)
    except Exception as e:
        print(f"An error occurred while fetching deeptrace top processes: {e}")


if __name__ == "__main__":
    main()
