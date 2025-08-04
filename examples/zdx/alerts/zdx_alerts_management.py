#!/usr/bin/env python

"""
zdx_alerts_management.py
========================

Manage Alerts for Zscaler Digital Experience (ZDX).

**Usage**::

    zdx_alerts_management.py [--use-legacy-client]

**Examples**:

Retrieve All Ongoing Alerts with Optional Filters (Defaults to the previous 2 hours):
    $ python3 zdx_alerts_management.py

Retrieve Historical Alerts with Optional Filters (Defaults to the previous 2 hours):
    $ python3 zdx_alerts_management.py

Retrieve Alert details including the impacted department, Zscaler locations, geolocation, and alert trigger:
    $ python3 zdx_alerts_management.py

Retrieve Alert details for affected Devices for specific AlertID:
    $ python3 zdx_alerts_management.py

Using Legacy Client:
    $ python3 zdx_alerts_management.py --use-legacy-client

"""

import os
import time
import logging
import argparse
from prettytable import PrettyTable
from zscaler import ZscalerClient
from zscaler.oneapi_client import LegacyZDXClient


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


def display_table(headers, data):
    table = PrettyTable(headers)
    for item in data:
        row = []
        for header in headers:
            key = header.lower().replace(" ", "_")
            if key == "device_id":
                key = "id"
            elif key == "device_name":
                key = "name"
            elif key == "user_id":
                key = "userid"
            row.append(item.get(key))
        table.add_row(row)
    print(table)


def display_alerts(alerts):
    print(f"Alerts received for display: {alerts}")  # Debugging print statement
    table = PrettyTable(
        ["ID", "Rule Name", "Severity", "Alert Type", "Status", "Num Geolocations", "Num Devices", "Started On", "Ended On"]
    )
    for alert in alerts:
        print(f"Processing alert: {alert}")  # Debugging print statement
        started_on = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(alert["started_on"]))
        ended_on = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(alert["ended_on"])) if alert["ended_on"] != 0 else "N/A"
        num_geolocations = len(alert.get("geolocations", []))
        num_devices = alert.get("num_devices", 0)
        table.add_row(
            [
                alert["id"],
                alert["rule_name"],
                alert["severity"],
                alert["alert_type"],
                alert["alert_status"],
                num_geolocations,
                num_devices,
                started_on,
                ended_on,
            ]
        )
    print(table)


def main():
    parser = argparse.ArgumentParser(description="Manage Alerts for Zscaler Digital Experience (ZDX)")
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

    # Prompt the user to choose an alert type
    print("Choose the Alert Type:")
    print("a. Retrieve All Ongoing Alerts with Optional Filters (Defaults to the previous 2 hours)")
    print("b. Retrieve Historical Alerts with Optional Filters (Defaults to the previous 2 hours)")
    print("c. Retrieve Alert details including the impacted department, Zscaler locations, geolocation, and alert trigger")
    print("d. Retrieve Alert details for affected Devices for specific AlertID")
    choice = input("Enter choice (a/b/c/d): ").strip()

    if choice in ["a", "b", "d"]:
        since = prompt_for_since()
    else:
        since = None

    if choice == "a":
        query_params = {}
        if since:
            query_params["since"] = since
        
        ongoing_alerts, _, err = client.zdx.alerts.list_ongoing(query_params=query_params)
        if err:
            print(f"Error listing ongoing alerts: {err}")
            return
        
        # Convert to list of dictionaries for display
        data = []
        for alert in ongoing_alerts:
            if hasattr(alert, 'as_dict'):
                data.append(alert.as_dict())
            else:
                data.append(alert)
        
        print(f"Data collected from API (ongoing alerts): {data}")  # Debugging print statement
        display_alerts(data)

    elif choice == "b":
        query_params = {}
        if since:
            query_params["since"] = since
        
        historical_alerts, _, err = client.zdx.alerts.list_historical(query_params=query_params)
        if err:
            print(f"Error listing historical alerts: {err}")
            return
        
        # Convert to list of dictionaries for display
        data = []
        for alert in historical_alerts:
            if hasattr(alert, 'as_dict'):
                data.append(alert.as_dict())
            else:
                data.append(alert)
        
        print(f"Data collected from API (historical alerts): {data}")  # Debugging print statement
        display_alerts(data)

    elif choice == "c":
        alert_id = input("Enter alert ID: ").strip()
        alert_details, _, err = client.zdx.alerts.get_alert(alert_id)
        if err:
            print(f"Error getting alert details: {err}")
            return
        
        if hasattr(alert_details, 'as_dict'):
            alert_details_dict = alert_details.as_dict()
        else:
            alert_details_dict = alert_details
        
        print(f"Alert details: {alert_details_dict}")  # Debugging print statement
        display_alerts([alert_details_dict])
        # Display impacted departments, locations, and geolocations
        print("\nImpacted Departments:")
        display_table(["Name", "Num Devices"], alert_details_dict.get("departments", []))
        print("\nImpacted Locations:")
        display_table(["Name", "Num Devices"], alert_details_dict.get("locations", []))
        print("\nGeolocations:")
        display_table(["Geolocation ID", "Num Devices"], alert_details_dict.get("geolocations", []))

    elif choice == "d":
        alert_id = input("Enter alert ID: ").strip()
        query_params = {}
        if since:
            query_params["since"] = since
        
        affected_devices, _, err = client.zdx.alerts.list_affected_devices(alert_id, query_params=query_params)
        if err:
            print(f"Error listing affected devices: {err}")
            return
        
        # Convert to list of dictionaries for display
        data = []
        for device in affected_devices:
            if hasattr(device, 'as_dict'):
                data.append(device.as_dict())
            else:
                data.append(device)
        
        headers = ["Device ID", "Device Name", "User ID", "User Name", "User Email"]
        print(f"Data collected from API (affected devices): {data}")  # Debugging print statement
        display_table(headers, data)

    else:
        print(f"Invalid choice: {choice}")


if __name__ == "__main__":
    main()
