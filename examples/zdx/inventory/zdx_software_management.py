#!/usr/bin/env python

"""
zdx_software_management.py
==========================

Manage Software for Zscaler Digital Experience (ZDX).

**Usage**::

    zdx_software_management.py

**Examples**:

Retrieve All Software with Optional Filters (Defaults to the previous 2 hours):
    $ python3 zdx_software_management.py

Retrieve Software Details for specific Software Key:
    $ python3 zdx_software_management.py

"""

import os
import time
import logging
import argparse
from prettytable import PrettyTable
from zscaler.zdx import ZDXClientHelper
from zscaler.zdx.inventory import InventoryAPI


def prompt_for_since():
    try:
        since_input = input("Enter the number of hours to look back (optional: Defaults to the previous 2 hours): ").strip()
        if since_input:
            return int(since_input)
        else:
            return 2  # Default to 2 hours
    except ValueError as e:
        print(f"Invalid input: {e}")
        exit(1)


def prompt_for_entries():
    try:
        entries_input = input("Enter the number of entries to display (optional: Defaults to all entries): ").strip()
        if entries_input:
            return int(entries_input)
        else:
            return None  # Default to displaying all entries
    except ValueError as e:
        print(f"Invalid input: {e}")
        exit(1)


def display_table(headers, data, max_entries=None):
    table = PrettyTable(headers)
    if max_entries:
        data = data[:max_entries]  # Limit the number of entries displayed
    for item in data:
        row = []
        for header in headers:
            key = header.lower().replace(" ", "_")
            row.append(item.get(key))
        table.add_row(row)

    # Set max width for each column
    table.max_width["Software Key"] = 30
    table.max_width["Software Name"] = 30
    table.max_width["Vendor"] = 20
    table.max_width["Software Group"] = 20
    table.max_width["Install Type"] = 10
    table.max_width["User Total"] = 10
    table.max_width["Device Total"] = 10

    print(table)


def display_softwares(softwares, max_entries=None):
    print(f"Softwares received for display: {softwares}")  # Debugging print statement
    table = PrettyTable(
        ["Software Key", "Software Name", "Vendor", "Software Group", "Install Type", "User Total", "Device Total"]
    )
    if max_entries:
        softwares = softwares[:max_entries]  # Limit the number of entries displayed
    for software in softwares:
        print(f"Processing software: {software}")  # Debugging print statement
        table.add_row(
            [
                software["software_key"],
                software["software_name"],
                software["vendor"],
                software["software_group"],
                software["sw_install_type"],
                software["user_total"],
                software["device_total"],
            ]
        )

    # Set max width for each column
    table.max_width["Software Key"] = 30
    table.max_width["Software Name"] = 30
    table.max_width["Vendor"] = 20
    table.max_width["Software Group"] = 20
    table.max_width["Install Type"] = 10
    table.max_width["User Total"] = 10
    table.max_width["Device Total"] = 10

    print(table)


def display_software_keys(software_keys, max_entries=None):
    print(f"Software keys received for display: {software_keys}")  # Debugging print statement
    table = PrettyTable(
        [
            "Software Key",
            "Software Name",
            "Version",
            "Software Group",
            "OS",
            "Vendor",
            "User ID",
            "Device ID",
            "Hostname",
            "Username",
            "Install Date",
        ]
    )
    if max_entries:
        software_keys = software_keys[:max_entries]  # Limit the number of entries displayed
    for key in software_keys:
        print(f"Processing software key: {key}")  # Debugging print statement
        install_date = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(int(key["install_date"])))
        table.add_row(
            [
                key["software_key"],
                key["software_name"],
                key["software_version"],
                key["software_group"],
                key["os"],
                key["vendor"],
                key["user_id"],
                key["device_id"],
                key["hostname"],
                key["username"],
                install_date,
            ]
        )

    # Set max width for each column
    table.max_width["Software Key"] = 30
    table.max_width["Software Name"] = 30
    table.max_width["Version"] = 20
    table.max_width["Software Group"] = 20
    table.max_width["OS"] = 20
    table.max_width["Vendor"] = 20
    table.max_width["User ID"] = 10
    table.max_width["Device ID"] = 10
    table.max_width["Hostname"] = 30
    table.max_width["Username"] = 20
    table.max_width["Install Date"] = 20

    print(table)


def main():
    parser = argparse.ArgumentParser(description="Manage Software for Zscaler Digital Experience (ZDX)")
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

    inventory_api = InventoryAPI(client)

    # Prompt the user to choose an option
    print("Choose the Software Option:")
    print("a. Retrieve All Software with Optional Filters (Defaults to the previous 2 hours)")
    print("b. Retrieve Software Details for specific Software Key")
    choice = input("Enter choice (a/b): ").strip()

    if choice in ["a", "b"]:
        max_entries = prompt_for_entries()

    if choice == "a":
        since = prompt_for_since()
        all_softwares = inventory_api.list_softwares(since=since)
        data = [software.to_dict() for software in all_softwares]
        print(f"Data collected from API (all softwares): {data}")  # Debugging print statement
        display_softwares(data, max_entries)

    elif choice == "b":
        software_key = input("Enter software key: ").strip()
        since = prompt_for_since()
        software_keys = inventory_api.list_software_keys(software_key, since=since)
        data = [key.to_dict() for key in software_keys]
        print(f"Data collected from API (software keys): {data}")  # Debugging print statement
        display_software_keys(data, max_entries)

    else:
        print(f"Invalid choice: {choice}")


if __name__ == "__main__":
    main()
