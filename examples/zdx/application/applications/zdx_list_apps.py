#!/usr/bin/env python

"""
zdx_list_apps.py
==========================

Retrieve a list of all active applications configured within the ZDX tenant.

**Usage**::

    zdx_list_apps.py [--use-legacy-client]

**Examples**:

Retrieve a list of applications with Optional Filters:
    $ python3 zdx_list_apps.py

Using Legacy Client:
    $ python3 zdx_list_apps.py --use-legacy-client

"""

import os
import time
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

    # Prompt the user for inputs
    since = prompt_for_since()
    location_id = prompt_for_input("Enter the location ID (optional): ", required=False)
    department_id = prompt_for_input("Enter the department ID (optional): ", required=False)
    geo_id = prompt_for_input("Enter the geolocation ID (optional): ", required=False)

    # Prepare query parameters
    query_params = {}
    if since:
        query_params["since"] = since
    if location_id:
        query_params["location_id"] = location_id
    if department_id:
        query_params["department_id"] = department_id
    if geo_id:
        query_params["geo_id"] = geo_id

    # Call the API and get the list of applications
    try:
        apps, _, err = client.zdx.apps.list_apps(query_params=query_params)
        if err:
            print(f"Error listing applications: {err}")
            return
        
        # Convert to list of dictionaries for display
        apps_data = []
        for app in apps:
            if hasattr(app, 'as_dict'):
                apps_data.append(app.as_dict())
            else:
                apps_data.append(app)
        
        print(f"Application data collected from API: {apps_data}")
        display_apps(apps_data)
    except Exception as e:
        print(f"An error occurred while fetching applications: {e}")


if __name__ == "__main__":
    main()
