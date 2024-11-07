#!/usr/bin/env python

"""
zdx_health_metrics_cli.py
====================

CLI tool to interact with ZDX Devices API to fetch health metrics.

**Usage**::

    zdx_health_metrics_cli.py

**Examples**:

Get health metrics for a device:
    $ python3 zdx_health_metrics_cli.py

Get health metrics for a device for the past 24 hours:
    $ python3 zdx_health_metrics_cli.py --since 24

"""

import os
import logging
import argparse
from prettytable import PrettyTable
from zscaler.zdx import ZDXClientHelper
from zscaler.zdx.devices import DevicesAPI
from box import Box


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


def extract_health_metrics_data(metrics):
    extracted_data = []
    for category in metrics:
        category_name = category.get("category")
        instances = category.get("instances", [])

        for instance in instances:
            instance_name = instance.get("name", "N/A")
            metrics = instance.get("metrics", [])

            for metric in metrics:
                metric_name = metric.get("metric")
                unit = metric.get("unit")
                datapoints = metric.get("datapoints", [])

                for datapoint in datapoints:
                    timestamp = datapoint.get("timestamp")
                    value = datapoint.get("value")
                    extracted_data.append([category_name, instance_name, metric_name, unit, value, timestamp])
    return extracted_data


def main():
    parser = argparse.ArgumentParser(description="Interact with ZDX Devices API to fetch health metrics")
    parser.add_argument("--since", type=int, help="The number of hours to look back for health metrics")

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

    # Prompt the user for device ID
    device_id = prompt_for_input("Enter the device ID: ")

    # Prepare keyword arguments
    kwargs = {
        "since": args.since,
    }

    # Remove None values from kwargs
    kwargs = {k: v for k, v in kwargs.items() if v is not None}

    # Call the API to get health metrics
    try:
        health_metrics = devices_api.get_health_metrics(device_id, **kwargs)
        headers = ["Category", "Instance", "Metric", "Unit", "Value", "Timestamp"]
        data = extract_health_metrics_data(health_metrics)
        display_table(data, headers)
    except Exception as e:
        print(f"An error occurred while fetching health metrics: {e}")


if __name__ == "__main__":
    main()
