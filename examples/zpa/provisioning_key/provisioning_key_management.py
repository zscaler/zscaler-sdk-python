#!/usr/bin/env python

# Copyright (c) 2023, Zscaler Inc.
#
# Permission to use, copy, modify, and/or distribute this software for any
# purpose with or without fee is hereby granted, provided that the above
# copyright notice and this permission notice appear in all copies.
#
# THE SOFTWARE IS PROVIDED "AS IS" AND THE AUTHOR DISCLAIMS ALL WARRANTIES
# WITH REGARD TO THIS SOFTWARE INCLUDING ALL IMPLIED WARRANTIES OF
# MERCHANTABILITY AND FITNESS. IN NO EVENT SHALL THE AUTHOR BE LIABLE FOR
# ANY SPECIAL, DIRECT, INDIRECT, OR CONSEQUENTIAL DAMAGES OR ANY DAMAGES
# WHATSOEVER RESULTING FROM LOSS OF USE, DATA OR PROFITS, WHETHER IN AN
# ACTION OF CONTRACT, NEGLIGENCE OR OTHER TORTIOUS ACTION, ARISING OUT OF
# OR IN CONNECTION WITH THE USE OR PERFORMANCE OF THIS SOFTWARE.

"""
provisioning_key_management.py
==============================

Manage Provisioning Keys for Zscaler Private Access (ZPA).

Usage:
    python provisioning_key_management.py [options]

Options:
    -l, --list [key_type]        List all provisioning keys of the specified type (connector or service_edge).
    -a, --add                    Add a new provisioning key. Prompts for additional details.
    -u, --update <key_id>        Update an existing provisioning key. Prompts for additional details.
    -d, --delete <key_id>        Delete a provisioning key by its ID.
    -h, --help                   Show this help message and exit.
"""

__author__ = "Your Name"
import argparse
import os
import json
from zscaler import ZPAClientHelper

# Initialize ZIAClientHelper with environment variables
ZPA_CLIENT_ID = os.getenv("ZPA_CLIENT_ID")
ZPA_CLIENT_SECRET = os.getenv("ZPA_CLIENT_SECRET")
ZPA_CUSTOMER_ID = os.getenv("ZPA_CUSTOMER_ID")
ZPA_CLOUD = os.getenv("ZPA_CLOUD")

client = ZPAClientHelper(
    client_id=ZPA_CLIENT_ID,
    client_secret=ZPA_CLIENT_SECRET,
    customer_id=ZPA_CUSTOMER_ID,
    cloud=ZPA_CLOUD,
)


def main():
    parser = argparse.ArgumentParser(description="Manage Provisioning Keys for ZPA.")
    parser.add_argument(
        "-l",
        "--list",
        nargs="?",
        const=True,
        help="List all provisioning keys of the specified type (connector or service_edge).",
    )
    parser.add_argument("-a", "--add", action="store_true", help="Add a new provisioning key.")
    parser.add_argument("-u", "--update", metavar="KEY_ID", help="Update an existing provisioning key.")
    parser.add_argument("-d", "--delete", metavar="KEY_ID", help="Delete a provisioning key by its ID.")
    args = parser.parse_args()

    if args.list is not None:
        key_type = get_key_type()
        keys = client.provisioning.list_provisioning_keys(key_type)
        print(json.dumps(keys, indent=4))  # Serialize the list to JSON format
    elif args.add:
        add_provisioning_key(client)
    elif args.update:
        update_provisioning_key(client, args.update)
    elif args.delete:
        delete_provisioning_key(client, args.delete)
    else:
        parser.print_help()


def get_key_type():
    while True:
        choice = input("Select provisioning key type (1- Connector, 2- Service Edge): ").strip()
        if choice == "1":
            return "connector"
        elif choice == "2":
            return "service_edge"
        else:
            print("Invalid selection. Please choose 1 or 2.")


def add_provisioning_key(client):
    key_type = get_key_type()
    name = input("Enter the name of the provisioning key: ").strip()
    max_usage = input("Enter the max usage of the provisioning key: ").strip()
    component_id = input("Enter the component ID (Connector Group ID or Service Edge Group ID): ").strip()

    # Fetch enrollment certificates
    enrollment_certs = client.certificates.list_enrolment()

    cert_name = "Connector" if key_type == "connector" else "Service Edge"
    enrollment_cert_id = None
    for cert in enrollment_certs:
        if cert_name in cert.get("name", ""):
            enrollment_cert_id = cert.get("id")
            break

    if not enrollment_cert_id:
        print(f"No enrollment certificate found for '{cert_name}'.")
        return

    response = client.provisioning.add_provisioning_key(key_type, name, max_usage, enrollment_cert_id, component_id)
    print("Provisioning key added successfully:", response)


def update_provisioning_key(client, key_id):
    key_type = get_key_type()
    name = input("Enter the new name of the provisioning key (leave blank to skip): ").strip()
    kwargs = {"name": name} if name else {}

    client.provisioning.update_provisioning_key(key_id, key_type, **kwargs)
    print(f"Provisioning key {key_id} updated successfully.")


def delete_provisioning_key(client, key_id):
    key_type = get_key_type()
    client.provisioning.delete_provisioning_key(key_id, key_type)
    print(f"Provisioning key {key_id} deleted successfully.")


if __name__ == "__main__":
    main()
