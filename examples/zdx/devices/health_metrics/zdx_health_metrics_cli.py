#!/usr/bin/env python

"""
zdx_health_metrics_cli.py
====================

CLI tool to interact with ZDX Devices API to fetch health metrics.

**Usage**::

    zdx_health_metrics_cli.py [--use-legacy-client]

**Examples**:

Get health metrics for a device:
    $ python3 zdx_health_metrics_cli.py

Get health metrics for a device for the past 24 hours:
    $ python3 zdx_health_metrics_cli.py --since 24

Using Legacy Client:
    $ python3 zdx_health_metrics_cli.py --use-legacy-client

"""

import os
import logging
import argparse
from prettytable import PrettyTable
from zscaler import ZscalerClient
from zscaler.oneapi_client import LegacyZDXClient
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

    # Prompt the user for device ID
    device_id = prompt_for_input("Enter the device ID: ")

    # Prepare query parameters
    query_params = {}
    if args.since:
        query_params["since"] = args.since

    # Call the API to get health metrics
    try:
        health_metrics, _, err = client.zdx.devices.get_health_metrics(device_id, query_params=query_params)
        if err:
            print(f"Error retrieving health metrics: {err}")
            return
        
        if hasattr(health_metrics, 'as_dict'):
            metrics_data = health_metrics.as_dict()
        else:
            metrics_data = health_metrics
        
        headers = ["Category", "Instance", "Metric", "Unit", "Value", "Timestamp"]
        data = extract_health_metrics_data(metrics_data)
        display_table(data, headers)
    except Exception as e:
        print(f"An error occurred while fetching health metrics: {e}")


if __name__ == "__main__":
    main()
