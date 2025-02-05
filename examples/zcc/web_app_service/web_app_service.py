#!/usr/bin/env python3
"""
web_app_service_cli.py
======================

Retrieve WebAppService (Fail Open Policy) data from the ZCC Portal via the ZscalerClient.

**Usage**::

    web_app_service_cli.py [--search SEARCH_STR]

**Examples**:

1) Display all WebAppService items:
    $ python web_app_service_cli.py

2) Display only those matching a certain name:
    $ python web_app_service_cli.py --search "ZOOMMEETING"
"""

import os
import argparse
from prettytable import PrettyTable

from zscaler import ZscalerClient

# Example config dict. Adjust with your actual credentials.
config = {
    "clientId": os.getenv("ZSCALER_CLIENT_ID", ""),
    "clientSecret": os.getenv("ZSCALER_CLIENT_SECRET", ""),
    "vanityDomain": os.getenv("ZSCALER_VANITY_DOMAIN", ""),
    "customerId": os.getenv("ZPA_CUSTOMER_ID", ""),
    "logging": {
        "enabled": True,
        "verbose": True
    },
}

def prompt_for_input(prompt_message, required=True):
    """
    Prompt the user for input and ensure it is not empty if required.
    """
    while True:
        user_input = input(prompt_message).strip()
        if user_input or not required:
            return user_input
        print("This field is required.")


def display_policies(policies):
    """
    Display the list of policies in a table format.
    """
    if not policies:
        print("No policies found.")
        return

    # Create a table with columns
    table = PrettyTable()
    table.field_names = ["AppName", "Created By", "Edited By", "Edited Timestamp", "Version"]

    # Add rows to the table
    for policy in policies:
        table.add_row([
            policy.app_name,  # Use snake_case attribute name
            policy.created_by,  # Use snake_case attribute name
            policy.edited_by,   # Use snake_case attribute name
            policy.edited_timestamp,  # Use snake_case attribute name
            policy.version
        ])

    print(table)


def main():
    # Parse command-line arguments
    parser = argparse.ArgumentParser(description="Retrieve Web App Service Policies for Zscaler Client Connector (ZCC)")
    args = parser.parse_args()

    # Initialize Zscaler Client
    with ZscalerClient(config) as client:
        # Ask the user if they want to search for a specific policy
        search_policy = prompt_for_input("Do you want to search for a specific policy? (y/n): ").strip().lower()
        query_params = {}

        if search_policy in ["y", "yes"]:
            policy_name = prompt_for_input("Enter the policy name to search for: ")
            query_params["search"] = policy_name

        # Retrieve the list of policies
        result, response, error = client.zcc.web_app_service.list_by_company(query_params=query_params)
        if error:
            print(f"Error: {error}")
            return

        # Display the policies in table format
        display_policies(result)


if __name__ == "__main__":
    main()