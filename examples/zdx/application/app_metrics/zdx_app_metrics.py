#!/usr/bin/env python

"""
zdx_app_metrics.py
==========================

Retrieve Application Metrics for Zscaler Digital Experience (ZDX).

**Usage**::

    zdx_app_metrics.py

**Examples**:

Retrieve Application Metrics with Optional Filters:
    $ python zdx_app_metrics.py

"""

import os
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


def display_metrics(metrics):
    if not metrics:
        print("No metrics data available.")
        return

    table = PrettyTable(["Metric", "Unit", "Datapoints"])
    for metric in metrics:
        table.add_row([metric["metric"], metric["unit"], metric["datapoints"]])

    print(table)


def main():
    parser = argparse.ArgumentParser(description="Retrieve Application Metrics for Zscaler Digital Experience (ZDX)")
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
    metric_name = prompt_for_input("Enter the metric name (optional: pft, dns, availability): ", required=False)
    location_id = prompt_for_input("Enter the location ID (optional): ", required=False)
    department_id = prompt_for_input("Enter the department ID (optional): ", required=False)
    geo_id = prompt_for_input("Enter the geolocation ID (optional): ", required=False)

    # Prepare keyword arguments
    kwargs = {
        "since": since,
        "metric_name": metric_name,
        "location_id": location_id,
        "department_id": department_id,
        "geo_id": geo_id,
    }

    # Remove None values from kwargs
    kwargs = {k: v for k, v in kwargs.items() if v is not None}

    # Call the API and get the metrics
    try:
        metrics = apps_api.get_app_metrics(app_id=app_id, **kwargs)
        print(f"Metrics data collected from API: {metrics}")
        display_metrics(metrics)
    except Exception as e:
        print(f"An error occurred while fetching metrics: {e}")


if __name__ == "__main__":
    main()
