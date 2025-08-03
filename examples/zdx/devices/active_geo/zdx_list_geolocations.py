#!/usr/bin/env python

"""
zdx_list_geolocations.py
==========================

Retrieve a list of all active geolocations configured within the ZDX tenant.

**Usage**::

    zdx_list_geolocations.py [--use-legacy-client]

**Examples**:

Retrieve a list of geolocations with Optional Filters:
    $ python zdx_list_geolocations.py

Using Legacy Client:
    $ python zdx_list_geolocations.py --use-legacy-client

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


def display_geolocations(geolocations):
    if not geolocations:
        print("No geolocation data available.")
        return

    table = PrettyTable(["ID", "Name", "Geo Type"])
    for geo in geolocations:
        geo_id = geo.get("id")
        name = geo.get("name")
        geo_type = geo.get("geo_type")

        table.add_row([geo_id, name, geo_type])

    print(table)


def main():
    parser = argparse.ArgumentParser(description="Retrieve a list of all active geolocations configured within the ZDX tenant")
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
    parent_geo_id = prompt_for_input("Enter the parent geolocation ID (optional): ", required=False)
    search = prompt_for_input("Enter the search string to filter by name (optional): ", required=False)

    # Prepare query parameters
    query_params = {}
    if since:
        query_params["since"] = since
    if location_id:
        query_params["location_id"] = location_id
    if parent_geo_id:
        query_params["parent_geo_id"] = parent_geo_id
    if search:
        query_params["search"] = search

    # Call the API and get the list of geolocations
    try:
        geolocations, _, err = client.zdx.devices.list_geolocations(query_params=query_params)
        if err:
            print(f"Error listing geolocations: {err}")
            return
        
        # Convert to list of dictionaries for display
        geolocations_data = []
        for geo in geolocations:
            if hasattr(geo, 'as_dict'):
                geolocations_data.append(geo.as_dict())
            else:
                geolocations_data.append(geo)
        
        print(f"Geolocation data collected from API: {geolocations_data}")
        display_geolocations(geolocations_data)
    except Exception as e:
        print(f"An error occurred while fetching geolocations: {e}")


if __name__ == "__main__":
    main()
