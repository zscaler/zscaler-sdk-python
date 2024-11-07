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
saml_attribute_management.py
============================

Manages SAML Attributes for Zscaler Private Access (ZPA).

**Usage**:
    python3 saml_attribute_management.py [-h] [-l] [-g ATTRIBUTE_ID] [--list_by_idp_name IDP_NAME] [--search_name ATTRIBUTE_NAME]

**Options**:
    -h, --help              Show this help message and exit.
    -l, --list              List all SAML attributes.
    -g, --get ATTRIBUTE_ID  Get details of a SAML attribute by its ID.
    --list_by_idp_name IDP_NAME List all SAML attributes by IdP name.
    --search_name ATTRIBUTE_NAME Search a SAML attribute by its name.

**Examples**:
    Listing all SAML Attributes:
        $ python3 saml_attribute_management.py -l

    Getting details of a SAML Attribute by Name:
        $ python3 saml_attribute_management.py --search_name "ATTRIBUTE_NAME"

    Getting details of a SAML Attribute by ID:
        $ python3 saml_attribute_management.py -g "ATTRIBUTE_ID"

    Listing all SAML Attributes by IDP Name:
        $ python3 saml_attribute_management.py --list_by_idp_name "IDP_NAME"
"""

import argparse
import json
import os
from zscaler import ZPAClientHelper


def main():
    parser = argparse.ArgumentParser(description="Retrieves SAML Attributes from the ZPA cloud.")
    parser.add_argument("-l", "--list", action="store_true", help="List all SAML attributes.")
    parser.add_argument(
        "-g",
        "--get",
        metavar="ATTRIBUTE_ID",
        help="Get details of a SAML attribute by its ID.",
    )
    parser.add_argument(
        "--list_by_idp_name",
        metavar="IDP_NAME",
        help="List all SAML attributes by IdP name.",
    )
    parser.add_argument(
        "--search_name",
        metavar="ATTRIBUTE_NAME",
        help="Search a SAML attribute by its name.",
    )
    args = parser.parse_args()

    client = ZPAClientHelper(
        client_id=os.getenv("ZPA_CLIENT_ID"),
        client_secret=os.getenv("ZPA_CLIENT_SECRET"),
        customer_id=os.getenv("ZPA_CUSTOMER_ID"),
        cloud=os.getenv("ZPA_CLOUD"),
    )

    if args.list:
        list_attributes(client)
    elif args.get:
        get_attribute(client, args.get)
    elif args.list_by_idp_name:
        list_attributes_by_idp_name(client, args.list_by_idp_name)
    elif args.search_name:
        search_attribute_by_name(client, args.search_name)


def list_attributes(client):
    attributes = client.saml_attributes.list_attributes()
    print(json.dumps(attributes, indent=4))


def get_attribute(client, attribute_id):
    attribute = client.saml_attributes.get_attribute(attribute_id)
    print(json.dumps(attribute, indent=4))


def list_attributes_by_idp_name(client, idp_name):
    idp = client.idp.get_idp_by_name(idp_name)
    if idp:
        idp_id = idp["id"]
        attributes = client.saml_attributes.list_attributes_by_idp(idp_id)
        print(json.dumps(attributes, indent=4))
    else:
        print(f"No IdP found with name {idp_name}")


def search_attribute_by_name(client, attribute_name):
    attributes = client.saml_attributes.list_attributes()
    filtered_attributes = [attr for attr in attributes if attr["name"] == attribute_name]
    print(
        json.dumps(filtered_attributes, indent=4)
        if filtered_attributes
        else f"No SAML attribute found with name {attribute_name}"
    )


if __name__ == "__main__":
    main()
