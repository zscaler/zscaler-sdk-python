#!/usr/bin/env python

"""
zdx_alerts_management.py
========================

Manage Alerts for Zscaler Digital Experience (ZDX).

**Usage**::

    zdx_alerts_management.py

**Examples**:

Retrieve All Ongoing Alerts with Optional Filters (Defaults to the previous 2 hours):
    $ python3 zdx_alerts_management.py

Retrieve Historical Alerts with Optional Filters (Defaults to the previous 2 hours):
    $ python3 zdx_alerts_management.py

Retrieve Alert details including the impacted department, Zscaler locations, geolocation, and alert trigger:
    $ python3 zdx_alerts_management.py

Retrieve Alert details for affected Devices for specific AlertID:
    $ python3 zdx_alerts_management.py

"""

import os
import time
import logging
import argparse
from prettytable import PrettyTable
from zscaler.zdx import ZDXClientHelper
from zscaler.zdx.alerts import AlertsAPI


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

    alerts_api = AlertsAPI(client)

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
        ongoing_alerts = alerts_api.list_ongoing(since=since)
        data = [alert for alert in ongoing_alerts]
        print(f"Data collected from API (ongoing alerts): {data}")  # Debugging print statement
        display_alerts(data)

    elif choice == "b":
        historical_alerts = alerts_api.list_historical(since=since)
        data = [alert for alert in historical_alerts]
        print(f"Data collected from API (historical alerts): {data}")  # Debugging print statement
        display_alerts(data)

    elif choice == "c":
        alert_id = input("Enter alert ID: ").strip()
        alert_details = alerts_api.get_alert(alert_id).to_dict()
        print(f"Alert details: {alert_details}")  # Debugging print statement
        display_alerts([alert_details])
        # Display impacted departments, locations, and geolocations
        print("\nImpacted Departments:")
        display_table(["Name", "Num Devices"], alert_details.get("departments", []))
        print("\nImpacted Locations:")
        display_table(["Name", "Num Devices"], alert_details.get("locations", []))
        print("\nGeolocations:")
        display_table(["Geolocation ID", "Num Devices"], alert_details.get("geolocations", []))

    elif choice == "d":
        alert_id = input("Enter alert ID: ").strip()
        affected_devices = alerts_api.list_affected_devices(alert_id, since=since)
        data = [device.to_dict() for device in affected_devices]
        headers = ["Device ID", "Device Name", "User ID", "User Name", "User Email"]
        print(f"Data collected from API (affected devices): {data}")  # Debugging print statement
        display_table(headers, data)

    else:
        print(f"Invalid choice: {choice}")


if __name__ == "__main__":
    main()
