#!/usr/bin/env python

"""
zdx_app_score.py
==========================

Retrieve Application Score for Zscaler Digital Experience (ZDX).

**Usage**::

    zdx_app_score.py [--use-legacy-client]

**Examples**:

Retrieve Application Score with Optional Filters:
    $ python3 zdx_app_score.py

Using Legacy Client:
    $ python3 zdx_app_score.py --use-legacy-client

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


def display_scores(scores):
    if not scores or "datapoints" not in scores:
        print("No score data available.")
        return

    datapoints = scores["datapoints"]
    table = PrettyTable(["Metric", "Unit", "Timestamp", "Value"])
    metric = scores.get("metric", "score")
    unit = scores.get("unit", "")

    for point in datapoints:
        timestamp = point["timestamp"]
        value = point["value"]
        table.add_row([metric, unit, timestamp, value])

    print(table)


def main():
    parser = argparse.ArgumentParser(description="Retrieve Application Score for Zscaler Digital Experience (ZDX)")
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
    app_id = prompt_for_input("Enter the Application ID: ")
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

    # Call the API and get the scores
    try:
        scores, _, err = client.zdx.apps.get_app_score(app_id, query_params=query_params)
        if err:
            print(f"Error retrieving app score: {err}")
            return
        
        if hasattr(scores, 'as_dict'):
            scores_dict = scores.as_dict()
        else:
            scores_dict = scores
        
        print(f"Scores data collected from API: {scores_dict}")
        display_scores(scores_dict)
    except Exception as e:
        print(f"An error occurred while fetching scores: {e}")


if __name__ == "__main__":
    main()
