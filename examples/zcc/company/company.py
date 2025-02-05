"""
zcc_company_info.py
==========================

Retrieve Company Information for Zscaler Client Connector (ZCC).

**Usage**::

    zcc_company_info.py

**Examples**:

Retrieve basic company information:
    $ python zcc_company_info.py

Show full details including nested configurations:
    $ python zcc_company_info.py
    Would you like to see full details? (y/n): y
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

def display_company_info(company_info, full_details=False):
    """Display company information in a structured format."""
    # Main Info Table
    main_table = PrettyTable()
    main_table.title = "Company Overview"
    main_table.field_names = ["Field", "Value"]
    main_table.align = "l"
    main_table.hrules = HRuleStyle.ALL  # Use HRuleStyle enum
    main_table.vrules = VRuleStyle.ALL  # Use VRuleStyle enum

    # Add basic fields (filter out complex structures)
    simple_fields = [
        'orgId', 'name', 'version', 'proxyPort', 
        'deviceGroupsCount', 'mdmStatus', 'dlpEnabled'
    ]
    
    for field in simple_fields:
        if field in company_info:
            main_table.add_row([field.title().replace("Id", "ID"), company_info[field]])

    print(main_table)

    if not full_details:
        return

    # Web App Config Table
    if 'webAppConfig' in company_info:
        webapp_table = PrettyTable()
        webapp_table.title = "Web Application Configuration"
        webapp_table.field_names = ["Configuration Key", "Value"]
        webapp_table.align = "l"
        webapp_table.max_width = 100

        for key, value in company_info['webAppConfig'].items():
            webapp_table.add_row([key, str(value)[:100]])  # Truncate long values

        print("\n" + webapp_table.get_string())

    # Device Posture Frequency Table
    if 'devicePostureFrequency' in company_info:
        posture_table = PrettyTable()
        posture_table.title = "Device Posture Frequency Settings"
        posture_table.field_names = [
            "Posture ID", "Posture Name", 
            "Windows Value", "Mac Value", "Default"
        ]

        for entry in company_info['devicePostureFrequency']:
            posture_table.add_row([
                entry.get('postureId'),
                entry.get('postureName'),
                entry.get('windowsValue'),
                entry.get('macValue'),
                entry.get('defaultValue')
            ])

        print("\n" + posture_table.get_string())

    # Additional Sections
    network_table = PrettyTable()
    network_table.title = "Network Settings"
    network_table.add_column("Setting", [])
    network_table.add_column("Value", [])
    
    network_fields = [
        ('proxyEnabled', 'Proxy Enabled'),
        ('zpnEnabled', 'ZPN Enabled'),
        ('enableZscalerFirewall', 'Zscaler Firewall'),
        ('disasterRecovery', 'Disaster Recovery')
    ]
    
    for field, label in network_fields:
        if field in company_info:
            network_table.add_row([label, company_info[field]])
    
    if network_table.rows:
        print("\n" + network_table.get_string())

def prompt_yes_no(question):
    """Simple yes/no prompt."""
    while True:
        response = input(f"{question} (y/n): ").lower()
        if response in ['y', 'n']:
            return response == 'y'
        print("Please enter 'y' or 'n'.")

def main():
    with ZscalerClient(config) as client:
        company_info = client.zcc.company.get_company_info()
        
        if not company_info:
            print("Error: Could not retrieve company information")
            return

        # Ask user for detail level
        full_details = prompt_yes_no("\nWould you like to see full details?")
        display_company_info(company_info, full_details)

if __name__ == "__main__":
    main()