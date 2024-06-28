#!/usr/bin/env python

"""
zdx_app_score.py
==========================

Retrieve Application Score for Zscaler Digital Experience (ZDX).

**Usage**::

    zdx_app_score.py

**Examples**:

Retrieve Application Score with Optional Filters:
    $ python3 zdx_app_score.py

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
    app_id = prompt_for_input("Enter the Application ID: ")
    since = prompt_for_since()
    location_id = prompt_for_input("Enter the location ID (optional): ", required=False)
    department_id = prompt_for_input("Enter the department ID (optional): ", required=False)
    geo_id = prompt_for_input("Enter the geolocation ID (optional): ", required=False)

    # Prepare keyword arguments
    kwargs = {"since": since, "location_id": location_id, "department_id": department_id, "geo_id": geo_id}

    # Remove None values from kwargs
    kwargs = {k: v for k, v in kwargs.items() if v is not None}

    # Call the API and get the scores
    try:
        scores = apps_api.get_app_score(app_id=app_id, **kwargs)
        print(f"Scores data collected from API: {scores}")
        display_scores(scores)
    except Exception as e:
        print(f"An error occurred while fetching scores: {e}")


if __name__ == "__main__":
    main()
