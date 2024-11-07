#!/usr/bin/env python

"""
zdx_list_apps.py
==========================

Retrieve a list of all active applications configured within the ZDX tenant.

**Usage**::

    zdx_list_apps.py

**Examples**:

Retrieve a list of applications with Optional Filters:
    $ python3 zdx_list_apps.py

"""

import os
import time
import logging
import argparse
from prettytable import PrettyTable
from zscaler.zdx import ZDXClientHelper
from zscaler.zdx.apps import AppsAPI


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


def display_apps(apps):
    if not apps:
        print("No application data available.")
        return

    table = PrettyTable(["App ID", "App Name", "Score", "Most Impacted Region", "Total Users"])
    for app in apps:
        app_id = app.get("id")
        name = app.get("name")
        score = app.get("score")
        most_impacted_region = app.get("most_impacted_region", {}).get("country", "N/A")
        total_users = app.get("total_users")

        table.add_row([app_id, name, score, most_impacted_region, total_users])

    print(table)


def main():
    parser = argparse.ArgumentParser(description="Retrieve a list of all active applications configured within the ZDX tenant")
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

    apps_api = AppsAPI(client)

    # Prompt the user for inputs
    since = prompt_for_since()
    location_id = prompt_for_input("Enter the location ID (optional): ", required=False)
    department_id = prompt_for_input("Enter the department ID (optional): ", required=False)
    geo_id = prompt_for_input("Enter the geolocation ID (optional): ", required=False)

    # Prepare keyword arguments
    kwargs = {"since": since, "location_id": location_id, "department_id": department_id, "geo_id": geo_id}

    # Remove None values from kwargs
    kwargs = {k: v for k, v in kwargs.items() if v is not None}

    # Call the API and get the list of applications
    try:
        apps_iterator = apps_api.list_apps(**kwargs)
        apps = list(apps_iterator)
        print(f"Application data collected from API: {apps}")
        display_apps(apps)
    except Exception as e:
        print(f"An error occurred while fetching applications: {e}")


if __name__ == "__main__":
    main()
