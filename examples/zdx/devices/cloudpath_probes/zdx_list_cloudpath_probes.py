#!/usr/bin/env python

"""
zdx_cloudpath_cli.py
====================

CLI tool to interact with ZDX Cloudpath APIs.

**Usage**::

    zdx_cloudpath_cli.py [--use-legacy-client]

**Examples**:

List all cloudpath probes for a device and application:
    $ python3 zdx_cloudpath_cli.py

Get details of a specific cloudpath probe:
    $ python3 zdx_cloudpath_cli.py

Get cloudpath data for a specific cloudpath probe:
    $ python3 zdx_cloudpath_cli.py

Using Legacy Client:
    $ python3 zdx_cloudpath_cli.py --use-legacy-client

"""

import os
import logging
import argparse
from prettytable import PrettyTable
from zscaler import ZscalerClient
from zscaler.oneapi_client import LegacyZDXClient
from box import BoxList


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


def display_table(data, headers):
    if not data:
        print("No data available.")
        return

    table = PrettyTable(headers)

    # Set column alignments
    table.align["Timestamp"] = "r"
    table.align["Leg SRC"] = "l"
    table.align["Leg DST"] = "l"
    table.align["Num Hops"] = "r"
    table.align["Latency"] = "r"
    table.align["Loss"] = "r"
    table.align["Num Unresp Hops"] = "r"
    table.align["Tunnel Type"] = "r"
    table.align["Hop IP"] = "l"
    table.align["GW MAC"] = "l"
    table.align["GW MAC Vendor"] = "l"
    table.align["Pkt Sent"] = "r"
    table.align["Pkt Rcvd"] = "r"
    table.align["Latency Min"] = "r"
    table.align["Latency Max"] = "r"
    table.align["Latency Avg"] = "r"
    table.align["Latency Diff"] = "r"

    for row in data:
        table.add_row(row)
    print(table)


def extract_probes_data(probes):
    extracted_data = []
    for probe in probes:
        probe_id = probe.get("id")
        name = probe.get("name")
        num_probes = probe.get("num_probes")
        avg_latencies = probe.get("avg_latencies", [])

        for latency in avg_latencies:
            leg_src = latency.get("leg_src")
            leg_dst = latency.get("leg_dst")
            latency_value = latency.get("latency")
            extracted_data.append([probe_id, name, num_probes, leg_src, leg_dst, latency_value])
    return extracted_data


def extract_probe_details(probes):
    extracted_data = []
    for probe in probes:
        leg_src = probe.get("leg_src")
        leg_dst = probe.get("leg_dst")
        stats = probe.get("stats", [])

        for stat in stats:
            metric = stat.get("metric")
            unit = stat.get("unit")
            datapoints = stat.get("datapoints", [])

            for datapoint in datapoints:
                timestamp = datapoint.get("timestamp")
                value = datapoint.get("value")
                extracted_data.append([leg_src, leg_dst, metric, unit, timestamp, value])
    return extracted_data


def extract_cloudpath_data(cloudpath_data):
    extracted_data = []
    for data_point in cloudpath_data:
        timestamp = data_point.get("timestamp")
        cloudpath = data_point.get("cloudpath", [])
        for path in cloudpath:
            leg_src = path.get("src")
            leg_dst = path.get("dst")
            num_hops = path.get("num_hops")
            latency = path.get("latency")
            loss = path.get("loss")
            num_unresp_hops = path.get("num_unresp_hops")
            tunnel_type = path.get("tunnel_type")
            hops = path.get("hops", [])

            for hop in hops:
                hop_ip = hop.get("ip")
                gw_mac = hop.get("gw_mac")
                gw_mac_vendor = hop.get("gw_mac_vendor")
                pkt_sent = hop.get("pkt_sent")
                pkt_rcvd = hop.get("pkt_rcvd")
                latency_min = hop.get("latency_min")
                latency_max = hop.get("latency_max")
                latency_avg = hop.get("latency_avg")
                latency_diff = hop.get("latency_diff")

                extracted_data.append(
                    [
                        timestamp,
                        leg_src,
                        leg_dst,
                        num_hops,
                        latency,
                        loss,
                        num_unresp_hops,
                        tunnel_type,
                        hop_ip,
                        gw_mac,
                        gw_mac_vendor,
                        pkt_sent,
                        pkt_rcvd,
                        latency_min,
                        latency_max,
                        latency_avg,
                        latency_diff,
                    ]
                )
    return extracted_data


def main():
    parser = argparse.ArgumentParser(description="Interact with ZDX Cloudpath APIs")
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

    # Prompt the user for action choice
    print("Choose an action:")
    print("a. List all cloudpath probes for a device and application")
    print("b. Get details of a specific cloudpath probe")
    print("c. Get cloudpath data for a specific cloudpath probe")
    action_choice = prompt_for_input("Enter choice (a/b/c): ")

    # Prompt the user for common inputs
    device_id = prompt_for_input("Enter the device ID: ")
    app_id = prompt_for_input("Enter the app ID: ")
    since = prompt_for_since()

    # Prepare query parameters
    query_params = {}
    if since:
        query_params["since"] = since

    if action_choice == "a":
        # Call the API to list cloudpath probes
        try:
            cloudpath_probes, _, err = client.zdx.devices.list_cloudpath_probes(device_id, app_id, query_params=query_params)
            if err:
                print(f"Error listing cloudpath probes: {err}")
                return
            
            # Convert to list of dictionaries for display
            probes_data = []
            for probe in cloudpath_probes:
                if hasattr(probe, 'as_dict'):
                    probes_data.append(probe.as_dict())
                else:
                    probes_data.append(probe)
            
            headers = ["ID", "Name", "Num Probes", "Leg SRC", "Leg DST", "Latency"]
            data = extract_probes_data(probes_data)
            display_table(data, headers)
        except Exception as e:
            print(f"An error occurred while fetching cloudpath probes: {e}")
    elif action_choice == "b":
        # Prompt the user for probe ID
        probe_id = prompt_for_input("Enter the probe ID: ")

        # Call the API to get cloudpath probe details
        try:
            cloudpath_probe, _, err = client.zdx.devices.get_cloudpath_probe(device_id, app_id, probe_id, query_params=query_params)
            if err:
                print(f"Error retrieving cloudpath probe details: {err}")
                return
            
            if hasattr(cloudpath_probe, 'as_dict'):
                probe_data = cloudpath_probe.as_dict()
            else:
                probe_data = cloudpath_probe
            
            headers = ["Leg SRC", "Leg DST", "Metric", "Unit", "Timestamp", "Value"]
            if isinstance(probe_data, BoxList):
                data = extract_probe_details(probe_data)
            else:
                data = extract_probe_details([probe_data])
            display_table(data, headers)
        except Exception as e:
            print(f"An error occurred while fetching cloudpath probe details: {e}")
    elif action_choice == "c":
        # Prompt the user for probe ID
        probe_id = prompt_for_input("Enter the probe ID: ")

        # Call the API to get cloudpath data
        try:
            cloudpath_data, _, err = client.zdx.devices.get_cloudpath(device_id, app_id, probe_id, query_params=query_params)
            if err:
                print(f"Error retrieving cloudpath data: {err}")
                return
            
            if hasattr(cloudpath_data, 'as_dict'):
                data_dict = cloudpath_data.as_dict()
            else:
                data_dict = cloudpath_data
            
            headers = [
                "Timestamp",
                "Leg SRC",
                "Leg DST",
                "Num Hops",
                "Latency",
                "Loss",
                "Num Unresp Hops",
                "Tunnel Type",
                "Hop IP",
                "GW MAC",
                "GW MAC Vendor",
                "Pkt Sent",
                "Pkt Rcvd",
                "Latency Min",
                "Latency Max",
                "Latency Avg",
                "Latency Diff",
            ]
            if isinstance(data_dict, BoxList):
                data = extract_cloudpath_data(data_dict)
            else:
                data = extract_cloudpath_data([data_dict])
            display_table(data, headers)
        except Exception as e:
            print(f"An error occurred while fetching cloudpath data: {e}")
    else:
        print("Invalid choice. Please enter 'a', 'b', or 'c'.")


if __name__ == "__main__":
    main()
