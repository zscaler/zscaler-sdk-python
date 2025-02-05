"""
add_trusted_network.py
==========================

This script provides a CLI tool for adding a new trusted network in Zscaler Client Connector (ZCC).

**Usage**::

    python add_trusted_network.py

**Examples**:

Add a new trusted network:
    $ python add_trusted_network.py
"""

from prettytable import PrettyTable, HRuleStyle, VRuleStyle
from zscaler import ZscalerClient
import os

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
    """Prompt the user for input and ensure it is not empty if required."""
    while True:
        user_input = input(prompt_message).strip()
        if user_input or not required:
            return user_input
        print("This field is required.")

def prompt_yes_no(question):
    """Simple yes/no prompt."""
    while True:
        response = input(f"{question} (y/n): ").lower()
        if response in ['y', 'n']:
            return response == 'y'
        print("Please enter 'y' or 'n'.")

def display_trusted_network(trusted_network):
    """Display the newly added trusted network in a table format."""
    if not trusted_network:
        print("No trusted network data available.")
        return

    table = PrettyTable()
    table.title = "New Trusted Network"
    table.field_names = ["Field", "Value"]
    table.align = "l"
    table.hrules = HRuleStyle.ALL  # Use HRuleStyle enum
    table.vrules = VRuleStyle.ALL  # Use VRuleStyle enum

    # Add rows to the table
    for key, value in trusted_network.as_dict().items():
        table.add_row([key, value])

    print(table)

def main():
    with ZscalerClient(config) as client:
        print("Adding a new trusted network...")

        # Prompt the user for inputs
        network_name = prompt_for_input("Enter the network name: ")
        dns_servers = prompt_for_input("Enter DNS servers (comma-separated): ")
        dns_search_domains = prompt_for_input("Enter DNS search domains (comma-separated): ", required=False)
        trusted_subnets = prompt_for_input("Enter trusted subnets (comma-separated): ", required=False)
        trusted_gateways = prompt_for_input("Enter trusted gateways (comma-separated): ", required=False)
        trusted_dhcp_servers = prompt_for_input("Enter trusted DHCP servers (comma-separated): ", required=False)
        active = prompt_yes_no("Should the network be active? (y/n): ")

        # Add the trusted network
        added_network, response, error = client.zcc.trusted_networks.add_trusted_network(
            active=active,
            network_name=network_name,
            dns_servers=dns_servers,
            dns_search_domains=dns_search_domains,
            trusted_subnets=trusted_subnets,
            trusted_gateways=trusted_gateways,
            trusted_dhcp_servers=trusted_dhcp_servers,
        )

        if error:
            print(f"Error adding trusted network: {error}")
            return

        # Display the newly added trusted network
        print("\nTrusted network added successfully!")
        display_trusted_network(added_network)

if __name__ == "__main__":
    main()