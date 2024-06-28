#!/usr/bin/env python

"""
zdx_list_geolocations.py
==========================

Retrieve a list of all active geolocations configured within the ZDX tenant.

**Usage**::

    zdx_list_geolocations.py

**Examples**:

Retrieve a list of geolocations with Optional Filters:
    $ python zdx_list_geolocations.py

"""

import os
import time
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

    # Prompt the user for inputs
    since = prompt_for_since()
    location_id = prompt_for_input("Enter the location ID (optional): ", required=False)
    parent_geo_id = prompt_for_input("Enter the parent geolocation ID (optional): ", required=False)
    search = prompt_for_input("Enter the search string to filter by name (optional): ", required=False)

    # Prepare keyword arguments
    kwargs = {"since": since, "location_id": location_id, "parent_geo_id": parent_geo_id, "search": search}

    # Remove None values from kwargs
    kwargs = {k: v for k, v in kwargs.items() if v is not None}

    # Call the API and get the list of geolocations
    try:
        geolocations_iterator = devices_api.list_geolocations(**kwargs)
        geolocations = list(geolocations_iterator)
        print(f"Geolocation data collected from API: {geolocations}")
        display_geolocations(geolocations)
    except Exception as e:
        print(f"An error occurred while fetching geolocations: {e}")


if __name__ == "__main__":
    main()
