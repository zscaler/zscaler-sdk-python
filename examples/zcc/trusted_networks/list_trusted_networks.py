"""
zcc_trusted_networks.py
==========================

Retrieve Trusted Networks for Zscaler Client Connector (ZCC).

**Usage**::

    zcc_trusted_networks.py

**Examples**:

Retrieve all trusted networks:
    $ python zcc_trusted_networks.py

Search for a specific trusted network by name:
    $ python zcc_trusted_networks.py
    Do you want to search for a specific trusted network? (y/n): y
    Enter the trusted network name to search for: BDTrustedNetwork01
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

def display_trusted_networks(trusted_networks):
    """Display trusted networks in a table format."""
    if not trusted_networks:
        print("No trusted networks found.")
        return

    # Create a table with columns
    table = PrettyTable()
    table.title = "Trusted Networks"
    table.field_names = [
        "ID", "Network Name", "Active", "DNS Servers", 
        "DNS Search Domains", "Trusted Subnets", "Trusted Gateways", 
        "Trusted DHCP Servers"
    ]
    table.align = "l"
    table.hrules = HRuleStyle.ALL  # Use HRuleStyle enum
    table.vrules = VRuleStyle.ALL  # Use VRuleStyle enum

    # Add rows to the table
    for network in trusted_networks:
        table.add_row([
            network.id,
            network.network_name,
            network.active,
            network.dns_servers,
            network.dns_search_domains,
            network.trusted_subnets,
            network.trusted_gateways,
            network.trusted_dhcp_servers
        ])

    print(table)

def prompt_yes_no(question):
    """Simple yes/no prompt."""
    while True:
        response = input(f"{question} (y/n): ").lower()
        if response in ['y', 'n']:
            return response == 'y'
        print("Please enter 'y' or 'n'.")

def main():
    with ZscalerClient(config) as client:
        # Ask the user if they want to search for a specific trusted network
        search_network = prompt_yes_no("Do you want to search for a specific trusted network?")
        query_params = {}

        if search_network:
            network_name = input("Enter the trusted network name to search for: ").strip()
            query_params["search"] = network_name

        # Retrieve the list of trusted networks
        trusted_networks, response, error = client.zcc.trusted_networks.list_by_company(query_params=query_params)
        if error:
            print(f"Error: {error}")
            return

        # Display the trusted networks in table format
        display_trusted_networks(trusted_networks)

if __name__ == "__main__":
    main()